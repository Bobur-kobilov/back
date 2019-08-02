from . import *

class CoinBlockHeight(APIView):
    """
    Coin Manager로 부터 CoinBlockHeight 값 가져오기
    """
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "coin-block-height"

    #--------------------------------------
    #  AUTHORITY
    #--------------------------------------
    permission_classes = [CoinBlockHeightPermission]


    def get(self, request, *args, **kwargs):
        coin = request.query_params.get("coin", None)

        manager = CoinManager()

        #try :
        result = manager.getCoinBlockHeight(coin)
        # except :
        #     return Response(
        #         data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00024.format(coin.upper()))
        #         , status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = {}
        data['coin'] = coin
        data['info'] = result

        return Response(data=data, status=status.HTTP_200_OK)