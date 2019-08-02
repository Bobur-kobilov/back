from . import *


class ModifyCoinAmountList(APIView):
    """
    코인수량 정정이력 생성
    """
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "modify-coin-amount"

    #--------------------------------------
    #  AUTHORITY
    #--------------------------------------
    permission_classes = [ModifyCoinListPermission]

    def get(self, request, *args, **kwargs):
        limit = request.query_params.get("limit", None)
        offset = request.query_params.get("offset", None)
        member_id = request.query_params.get("member_id", None)

        params = {}
        if member_id is not None:
            params['body.member_id'] = member_id

        data = {}

        mongodb = BCOfficeHistoryMongoDB(collection=TBL_BCOFFICE_MODIFY_COIN_AMOUNT)
        result = (mongodb.collection.find(params).sort('_id', pymongo.DESCENDING))
        count = mongodb.collection.find(params).count()

        if limit is not None and offset is not None:
            result = result[int(offset):int(offset) + int(limit)]
        data['count'] = count

        data['results'] = []

        for item in result :
            obj = {}
            obj['body'] = item['body']
            obj['body']['created_at'] = (datetime.strptime(obj['body']['created_at'], '%Y-%m-%d %H:%M:%S.%f')).strftime("%Y-%m-%d %H:%M:%S")

            data['results'].append(obj)

        mongodb.close()

        return Response(data = data, status = status.HTTP_200_OK)
