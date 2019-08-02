from . import *


class ColdWithdrawTxidUpdate(APIView):
    name = "cold_withdraw_txid_update"
    permission_classes  = [ColdWithdrawTxidUpdatePermission]

    def put(self, request, *args, **kwargs):
        withdarw_apply_id = request.data.get("withdraw_apply_id", None)
        txid = request.data.get("txid", None)

        if withdarw_apply_id is None :
            return Response(
                data = ResponseMessage.MESSAGE_ERR00017.format("withdraw_apply_id")
                , status=status.HTTP_400_BAD_REQUEST)

        if txid is None :
            return Response(
                data = ResponseMessage.MESSAGE_ERR00017.format("txid")
                , status=status.HTTP_400_BAD_REQUEST)

        history = WithdrawHistory.objects.get(withdraw_apply_id = withdarw_apply_id)

        if history is None :
            return Response(
                data = ResponseMessage.MESSAGE_ERR00008
                , status=status.HTTP_400_BAD_REQUEST)

        history.txid = txid
        history.save()

        return Response(
            data = ResponseMessage.MESSAGE_INF00002
            , status=status.HTTP_204_NO_CONTENT)