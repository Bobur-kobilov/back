from . import *

# 블랙리스트 목록조회

class BlackList(ListAPIView):
    # --------------------------------------
    #  PROPERTIES
    # --------------------------------------
    name = "blacklist"
    permission_classes = [BlackListPermission]

    def get(self, request, *args, **kwargs):

        # 페이지네이션
        limit = request.query_params.get('limit', None)
        offset = request.query_params.get('offset', None)
        state = request.query_params.get('state', None)
        type = request.query_params.get('type', None)
        value = request.query_params.get('value', None)
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)

        params = {}
        date_param = {}
        data = {}
        is_date_params = False

        if type is not None:
            params['type'] = type

        if value is not None:
            params['value'] = value

        if state is not None:
            params['state'] = state

        if start_date is not None:
            date_param['$gte'] = start_date + ' 00:00:00'
            is_date_params = True

        if end_date is not None:
            date_param['$lte'] = end_date + ' 24:00:00'
            is_date_params = True

        if is_date_params:
            params['updated_at'] = date_param

        # mongoDB 데이터 가져오기
        mongodb = BCOfficeBlackListMongoDB(collection=TBL_BCOFFICE_BLACKLIST_IP)

        result = (mongodb.collection.find(params).sort('_id', pymongo.DESCENDING))
        count = mongodb.collection.find(params).count()

        if limit is not None and offset is not None:
            result = result[int(offset):int(offset) + int(limit)]
            data['count'] = count

        data['results'] = []

        for item in result:
            obj = {}
            obj['type'] = item['type']
            obj['value']= item['ip']
            # obj['state'] = item['state']
            obj['user'] = User.objects.get(id=item['user']).email
            obj['reason'] = item['reason']
            obj['updated_at'] = item['updated_at']
            data['results'].append(obj)

        mongodb.close()

        return Response(data=data, status=status.HTTP_200_OK)