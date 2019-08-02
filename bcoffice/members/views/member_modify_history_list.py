from . import *

# 회원정보 정정이력
class MemberModifyHistoryList(APIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "member-history-list"
    permission_classes = [MemberModifyHistoryListPermission]

    def get(self, request, *args, **kwargs):
        
        # 페이지네이션
        limit           = request.query_params.get('limit', None)
        offset          = request.query_params.get('offset', None)

        # 회원정보로 검색
        member_id = request.query_params.get('member_id', None)

        start_date      = request.query_params.get('start_date', None)
        end_date        = request.query_params.get('end_date', None)

        params = {}
        date_param = {}
        data = {}
        is_date_params = False

        if member_id is not None:
            params['body.member_id'] = int(member_id)
        if start_date is not None :
            date_param['$gte'] = start_date
            is_date_params = True
        
        if  end_date is not None :
            date_param['$lte'] = end_date
            is_date_params = True

        if is_date_params :
            params['body.created_at'] = date_param

        # mongoDB 데이터 가져오기
        mongodb = BCOfficeHistoryMongoDB(collection=TBL_BCOFFICE_MEMBER_MOD)
        
        result = (mongodb.collection.find(params).sort('_id', pymongo.DESCENDING))
        count = mongodb.collection.find(params).count()
    
        if limit is not None and offset is not None:
            result = result[int(offset):int(offset) + int(limit)]
            data['count'] = count
        
        data['results'] = []

        for item in result :
            obj = {}
            obj['header'] = item['header']
            obj['header']['sqlTime'] =  obj['header']['sqlTime']
            obj['body'] = item['body']
            obj['body']['created_at'] = obj['body']['created_at']
            data['results'].append(obj)

        mongodb.close()
        
        return Response(data = data, status = status.HTTP_200_OK)