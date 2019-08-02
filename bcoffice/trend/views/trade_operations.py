from . import *
from rest_framework.exceptions import * 

class TradeOperationsList(APIView):
    """
    거래 운영
    """
    name = "trade-operations"
    permission_classes = [TradeOperationsPermission]
    pagination_class = LimitOffsetPagination

    def get_queryset(self, *args, **kwargs):
        date = kwargs.get('date', None)
        start_date = date + ' 00:00:00'
        end_date = date + ' 23:59:59'
        if start_date is None and end_date is None:
            raise ParseError('Invalid Dates')
        table = kwargs.get('table', None)
        if table == 'deposits':
            queryset = Deposits.objects.using('exchange').values('aasm_state') \
                .filter(created_at__range=(start_date, end_date)) \
                .annotate(count=Count('id'))
        elif table == 'withdraws':
            queryset = Withdraws.objects.using('exchange').values('aasm_state') \
                .filter(created_at__range=(start_date, end_date)) \
                .annotate(count=Count('id'))

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
        mongodb = BCOfficeMongoDB(__setting_name__='trend', collection=TBL_BCOFFICE_TRADE_OPERATIONS)
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
                'deposits': {
                    'total': 0,
                    'accepted': 0
                },
                'withdraws': {
                    'avg_processing_time': 0,
                    'system_block': 0,
                    'canceled': 0,
                    'manual_switch': 0,
                    'manual_done': 0,
                    'total': 0,
                    'done': 0
                }
            }
            dbCheck = mongo_result.count()
            dataExist = 0
            if dbCheck > 0:
                dataExist = len(mongo_result[0]['body']['results'])
            if dataExist == 0:
                # 입금
                deposits_queryset = self.get_queryset(date=current_date, table='deposits')
                for deposits in deposits_queryset:
                    daily_data['deposits']['total'] += deposits['count']
                    if deposits['aasm_state'] == 'accepted':
                        daily_data['deposits'][deposits['aasm_state']] = deposits['count']

                # 출금
                withdraws_queryset = self.get_queryset(date=current_date, table='withdraws')
                for withdraws in withdraws_queryset:
                    daily_data['withdraws']['total'] += withdraws['count']
                    if withdraws['aasm_state'] == 'done':
                        daily_data['withdraws'][withdraws['aasm_state']] = withdraws['count']
                    elif withdraws['aasm_state'] == 'canceled':
                        daily_data['withdraws'][withdraws['aasm_state']] = withdraws['count']

                # 결과값 MONGO DB 저장 (오늘이전날짜까지)
                if datetime.strptime(current_date, '%Y-%m-%d') < datetime.strptime(
                        datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d'):
                    body = {
                        "date": current_date
                        , "results": daily_data
                    }
                    # mongodb.insert_db(body)

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
        mongodb = BCOfficeMongoDB(__setting_name__='trend', collection=TBL_BCOFFICE_TRADE_OPERATIONS)
        mongodb.remove_db(init=True)
        mongodb.close()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def getMarketName(self, market_id=None):
        for market in settings.MARKET_LIST:
            if market['market_id'] == market_id:
                return market['name']
        return '-'