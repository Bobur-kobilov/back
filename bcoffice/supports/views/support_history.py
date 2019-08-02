from . import *


class SupportHistory(APIView):
    """
    고객 지원 내역
    """
    name = "support_history"
    permission_classes = [SupportHistoryPermission]
    pagination_class = LimitOffsetPagination

    def get_queryset(self, *args, **kwargs):
        date = kwargs.get('date', None)
        start_date = date + ' 00:00:00'
        end_date = date + ' 23:59:59'

        queryset = Question.objects.values('status') \
            .annotate(count=Count('id')) \
            .filter(created_at__range=(start_date, end_date)) \
            .order_by('status')

        return queryset

    def get(self, request, *args, **kwargs):
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
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
        mongodb = BCOfficeMongoDB(__setting_name__='trend', collection=TBL_BCOFFICE_SUPPORT_HISTORY)
        while True:
            # GET MONGO DB
            params = {}
            params['body.date'] = current_date
            mongo_result = (mongodb.collection.find(params).sort('_id', pymongo.DESCENDING))

            if mongo_result.count() is 0:
                # MONGO DB에 없는 경우 (MYSQL에서 추출 값을 MONGO DB에 저장 후 표기)
                daily_data = {}
                daily_data['date'] = current_date
                daily_data['question_accept'] = 0
                daily_data['question_cplt'] = 0
                daily_data['plus_accept'] = 0
                daily_data['plus_cplt'] = 0
                daily_data['mail_accept'] = 0
                daily_data['mail_cplt'] = 0
                daily_data['offline'] = 0
                daily_data['hacking_accept'] = 0
                daily_data['hacking_cplt'] = 0

                # 일일값 계산
                qa_queryset = self.get_queryset(date=current_date)
                for qa_count in qa_queryset:
                    daily_data['question_accept'] += qa_count['count']
                    if qa_count['status'].lower() == 'cplt':
                        daily_data['question_cplt'] += qa_count['count']

                # 결과값 MONGO DB 저장
                body = {
                    "date": current_date
                    , "results": daily_data
                }
                mongodb.insert_db(body)

                # result_data에 daily_data 추가
                result_data.append(daily_data)
            # MONGO DB에 있는 경우 (MONGO DB 값 그대로 누적)
            else:
                daily_data = mongo_result[0]['body']['results']
                daily_data['question_accept'] = 0
                daily_data['question_cplt'] = 0
                qa_queryset = self.get_queryset(date=current_date)
                for qa_count in qa_queryset:
                    daily_data['question_accept'] += qa_count['count']
                    if qa_count['status'].lower() == 'cplt':
                        daily_data['question_cplt'] += qa_count['count']
                body = {
                    "date": current_date
                    , "results": daily_data
                }
                mongodb.update_db(key='body.date', key_value=daily_data['date'], update_data=body)
                    
                # result_data에 daily_data 추가
                result_data.append(daily_data)

            # 마감일까지 실행하면 종료
            if datetime.strptime(current_date, '%Y-%m-%d') <= datetime.strptime(start_date, '%Y-%m-%d'):
                break
            else:
                current_date = (datetime.strptime(current_date, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')

        mongodb.close()

        return Response(data={'count': count, 'results': result_data})

    def put(self, request, *args, **kwargs):
        put_data = request.data.get('put_data')
        mongodb = BCOfficeMongoDB(__setting_name__='trend', collection=TBL_BCOFFICE_SUPPORT_HISTORY)

        today = (datetime.today().date()).strftime('%Y-%m-%d')
        if put_data['date'] == today:
            qa_queryset = self.get_queryset(date=today)
            put_data['results']['question_accept'] = 0
            put_data['results']['question_cplt'] = 0
            for qa_count in qa_queryset:
                put_data['results']['question_accept'] += qa_count['count']
                if qa_count['status'].lower() == 'cplt':
                    put_data['results']['question_cplt'] += qa_count['count']
        mongodb.update_db(key='body.date', key_value=put_data['date'], update_data=put_data)
        mongodb.close()

        return Response(data=put_data)