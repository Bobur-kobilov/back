from . import *
from rest_framework.exceptions import * 

class ReferralStatusList(APIView):
    # 레퍼럴 현황
    name = "referral-status"
    permission_classes = [ReferralStatusPermission]
    pagination_class = LimitOffsetPagination

    def get_queryset(self, *args, **kwargs):
        date = kwargs.get('date', None)
        start_date = date + ' 00:00:00'
        end_date = date + ' 23:59:59'

        queryset = ReferralFeeHistories.objects.using('exchange').values('currency', 'fee') \
            .annotate(amount=Sum('amount')) \
            .filter(created_at__range=(start_date, end_date)) \
            .order_by('currency')
        return queryset

    def get(self, request, *args, **kwargs):
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        if start_date is None and end_date is None:
           return Response(data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00033), status=status.HTTP_400_BAD_REQUEST)
        count = (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days + 1
        limit = request.query_params.get('limit', 10)
        offset = request.query_params.get('offset', 0)
        current_date = (datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=int(offset))).strftime('%Y-%m-%d')
        last_date = datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=int(limit) + int(offset) - 1)
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        if last_date > start_date:
            start_date = last_date
        start_date = start_date.strftime('%Y-%m-%d')

        result_data = []
        mongodb = BCOfficeMongoDB(__setting_name__='trend', collection=TBL_BCOFFICE_REFERRAL_STATUS)
        if mongodb is None:
            return Response(data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00034), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        while True:
            # GET MONGO DB
            params = {}
            params['body.date'] = current_date
            mongo_result = (mongodb.collection.find(params).sort('_id', pymongo.DESCENDING))

            # MONGO DB에 없는 경우 (MYSQL에서 추출 값을 MONGO DB에 저장 후 표기)
            daily_data = {
                'date': current_date,
                'new_referrals': Referrals.objects.using('exchange').filter(created_at__range=(current_date+' 00:00:00', current_date+' 23:59:59')).count(),
                'total_referrals': Referrals.objects.using('exchange').filter(created_at__lte=current_date+' 23:59:59').count(),
                'referrals': []
            }

            dbCheck = mongo_result.count()
            dataExist = 0
            if dbCheck > 0:
                dataExist = len(mongo_result[0]['body']['results'])
            if dataExist == 0:
                referral_fee_history_queryset = self.get_queryset(date=current_date)
                for referral_fee in referral_fee_history_queryset:
                    append_flag = True
                    for referrals in daily_data['referrals']:
                        if referrals['currency'] == referral_fee['currency']:
                            referrals['fee_rate_{}'.format(int(float(referral_fee['fee'])*100))] = float(referral_fee['amount'])
                            append_flag = False
                    if append_flag:
                        daily_data['referrals'].append({
                            'currency': referral_fee['currency'],
                            'fee_rate_{}'.format(int(float(referral_fee['fee'])*100)): float(referral_fee['amount'])
                        })

                # 결과값 MONGO DB 저장 (오늘이전날짜까지)
                if datetime.strptime(current_date, '%Y-%m-%d') < datetime.strptime(
                        datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d'):
                    body = {
                        "date": current_date
                        , "results": daily_data
                    }
                    mongodb.insert_db(body)

                # result_data에 daily_data 추가
                result_data.append(daily_data)
            # MONGO DB에 있는 경우 (MONGO DB 값 그대로 누적)
            else:
                for obj in mongo_result:
                    daily_data = obj['body']['results']
                # result_data에 daily_data 추가
                result_data.append(daily_data)

            # 마감일까지 실행하면 종료
            if datetime.strptime(current_date, '%Y-%m-%d') <= datetime.strptime(start_date, '%Y-%m-%d'):
                break
            else:
                current_date = (datetime.strptime(current_date, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')

        mongodb.close()

        return Response(data={'count': count, 'results': result_data})

    def delete(self, request, *args, **kwargs):
        mongodb = BCOfficeMongoDB(__setting_name__='trend', collection=TBL_BCOFFICE_REFERRAL_STATUS)
        mongodb.remove_db(init=True)
        mongodb.close()
        return Response(status=status.HTTP_204_NO_CONTENT)