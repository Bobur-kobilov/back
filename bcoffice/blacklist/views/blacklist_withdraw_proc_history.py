from . import *


# 블랙리스트 출금 내역조회

class BlackListWithdrawProcHistory(ListAPIView):
    # --------------------------------------
    #  PROPERTIES
    # --------------------------------------
    name = "blacklist-withdraw-proc-history"
    permission_classes = [BlackListWithdrawAddrListPermission]

    def get(self, request, *args, **kwargs):
        withdraw_id = request.query_params.get('withdraw_id', None)

        params = {}
        data = {}

        if withdraw_id is None:
            return Response(
                data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00017.format("withdraw_id"))
                , status=status.HTTP_400_BAD_REQUEST)

        params['withdraw_id'] = int(withdraw_id)

        # mongoDB 데이터 가져오기
        mongodb = BCOfficeBlackListMongoDB(collection=TBL_BCOFFICE_BLACKLIST_WITHDRAW_PROC)
        results = mongodb.collection.find(params)

        data['results'] = []

        result = results[0]
        for item in reversed(result['history']):
            obj = {}
            obj['type'] = item['type']
            obj['user'] = User.objects.get(id=item['user']).email
            obj['reason'] = item['reason']
            obj['created_at'] = item['created_at']
            data['results'].append(obj)

        mongodb.close()

        return Response(data=data, status=status.HTTP_200_OK)
