from . import *
from bcoffice.utils.coin_util import CoinUtil
from rest_framework.exceptions import * 
class DailyDepositWithdrawList(APIView):
    """
    일자별 입출금 내역
    """
    name = "daliy_deposit_withdraw"
    permission_classes  = [DailyDepositWithdrawPermission]
    pagination_class    = LimitOffsetPagination

    def get_queryset(self, *args, **kwargs):
        date = kwargs.get('date', None)
        start_date = date + ' 00:00:00'
        end_date = date + ' 23:59:59'

        table_type = kwargs.get('table_type', None)
        if table_type == 'withdraws':
            queryset = Withdraws.objects.using('exchange').values('currency') \
                .filter(aasm_state='done') \
                .filter(updated_at__range=(start_date, end_date)) \
                .annotate(withdraws_count=Count('id')) \
                .annotate(withdraws_sum=Sum('amount')) \
                .order_by('currency')
        elif table_type == 'deposits':
            queryset = Deposits.objects.using('exchange').values('currency') \
                .filter(aasm_state='accepted') \
                .filter(updated_at__range=(start_date, end_date)) \
                .annotate(deposits_count=Count('id')) \
                .annotate(deposits_sum=Sum('amount')) \
                .order_by('currency')
        return queryset

    def get(self, request, *args, **kwargs):
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        #Exception handling
        if start_date is None and end_date is None:
            return Response(data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00033), status=status.HTTP_400_BAD_REQUEST)
        result_data = []
        mongodb = BCOfficeMongoDB(__setting_name__='trend' ,collection=TBL_BCOFFICE_DAILY_DEPOSIT_WITHDRAW)
        if mongodb is None:
            return Response(data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00034), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        while True:
            # GET MONGO DB
            params = {}
            params['body.date'] = start_date
            mongo_result = (mongodb.collection.find(params).sort('_id', pymongo.DESCENDING))
            daily_data = [] 
    
            dbCheck = mongo_result.count()
            dataExist = 0
            #check whether data exists in the body part of MONGO DB response
            if dbCheck > 0:
                dataExist = len(mongo_result[0]['body']['results'])

            # MONGO DB에 없는 경우 (MYSQL에서 추출 값을 MONGO DB에 저장 후 표기)
            if dataExist == 0:  # https://stackoverflow.com/a/133024
                # 일일값 계산 (mysql - deposits, withdraws)
                deposits_queryset = self.get_queryset(table_type='deposits', date=start_date)
                withdraws_queryset = self.get_queryset(table_type='withdraws', date=start_date)
                daily_data = self.mergeListData(deposits_queryset, withdraws_queryset)
                # 결과값 MONGO DB 저장 (오늘이전날짜까지)
                if datetime.strptime(start_date, '%Y-%m-%d') < datetime.strptime(datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d'):
                    body = {
                        "date": start_date
                        , "results": daily_data
                    }    
                    mongodb.insert_db(body)

                # result_data에 daily_data 추가
                result_data = self.mergeListData(result_data, daily_data)
            # MONGO DB에 있는 경우 (MONGO DB 값 그대로 누적)
            else:
                for obj in mongo_result:
                    #check if dict is empty or not
                    if len(obj['body']['results']) > 0:
                        daily_data = obj['body']['results']
                # result_data에 daily_data 추가
                result_data = self.mergeListData(result_data, daily_data)
            # 마감일까지 실행하면 종료
            if start_date == end_date:
                break
            else:
                start_date = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')

        mongodb.close()
        return Response(data={'results': result_data})

    def delete(self, request, *args, **kwargs):
        mongodb = BCOfficeMongoDB(__setting_name__='trend', collection=TBL_BCOFFICE_DAILY_DEPOSIT_WITHDRAW)
        mongodb.remove_db(init=True)
        mongodb.close()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # 리스트 내부 값 합치기
    def mergeListData(self, a_list=[], b_list=[]):
        # 코인 목록
        currency_list = []
        for obj in a_list:
            currency_list.append(obj['currency'])
        for obj in b_list:
            currency_list.append(obj['currency'])
        currency_list = list(set(currency_list))  # 중복제거
        currency_list.sort(reverse=False)  # 정렬

        a_list_flag = 0
        b_list_flag = 0
        merge_list = []
        for currency in currency_list:
            is_append = False
            append_data = {  # 코인별 값
                'currency': currency
                , 'deposits_count': 0
                , 'deposits_sum': 0
                , 'withdraws_count': 0
                , 'withdraws_sum': 0
            }

            if len(a_list) > a_list_flag:
                a_obj = a_list[a_list_flag]
                if a_obj['currency'] == currency:
                    for key in a_obj:
                        if key != 'currency':
                            append_data[key] += float(a_obj[key])
                    a_list_flag += 1
                    is_append = True
            if len(b_list) > b_list_flag:
                b_obj = b_list[b_list_flag]
                if b_obj['currency'] == currency:
                    for key in b_obj:
                        if key != 'currency':
                            append_data[key] += float(b_obj[key])
                    b_list_flag += 1
                    is_append = True

            if is_append:
                merge_list.append(append_data)

        return merge_list
