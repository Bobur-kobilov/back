from . import *


class CoinBlanace(APIView):
    """
    지갑주소별 잔고 가져오기
    """
    name = "coin-balance"
    permission_classes = [CoinBalancePermission]

    def get(self, request, *args, **kwargs):
        wallet_address = request.query_params.get("wallet_address", None)
        currency_id = request.query_params.get("currency", None)

        balance = CoinUtil.getCoinBalance(currency_id, wallet_address)

        if balance is None:
            return Response(data=None, status=status.HTTP_204_NO_CONTENT)

        return Response(data={"balance": balance}, status=status.HTTP_200_OK)