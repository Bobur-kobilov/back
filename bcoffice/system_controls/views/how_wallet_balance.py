from . import *

class HotWalletBlanace(APIView):
    """
    핫월렛 코인별 잔고 가져오기
    """
    name = "coin-balance"
    permission_classes = [CoinBalancePermission]

    def get(self, request, *args, **kwargs):
        currency_id = request.query_params.get("currency", None)

        manager = CoinManager()
        coin_name = manager.transCurrencyIdToName(currency_id)

        if coin_name is None :
            return Response(data=None, status=status.HTTP_204_NO_CONTENT)

        balance = float( manager.getCoinBalance(coin_name)['result'] )

        if balance is None :
            return Response(data=None, status=status.HTTP_204_NO_CONTENT)

        return Response(data={"balance": balance}, status=status.HTTP_200_OK)