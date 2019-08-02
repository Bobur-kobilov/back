from . import *

# 블랙리스트 IP 제한 내역조회

class BlackListHistory(ListAPIView):
    # --------------------------------------
    #  PROPERTIES
    # --------------------------------------
    name = "blacklist-history"
    permission_classes = [BlackListPermission]


    def get(self, request, *args, **kwargs):
        value = request.query_params.get('value', None)
        type = request.query_params.get('type', None)

        params = {}
        params['type'] = type
        if value is not None:
            params['value'] = value

        # mongoDB 데이터 가져오기
        mongodb = BCOfficeBlackListMongoDB(collection=TBL_BCOFFICE_BLACKLIST)
        results = mongodb.collection.find(params)

        data = {}
        data['results'] = []

        result = results[0]
        for item in reversed(result['history']):
            obj = {}
            obj['state']         = item['state']
            obj['user']         = User.objects.get(id=item['user']).email
            obj['reason']       = item['reason']
            obj['created_at']   = item['created_at']
            data['results'].append(obj)

        mongodb.close()

        return Response(data=data, status=status.HTTP_200_OK)

