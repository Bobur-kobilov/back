from . import *
from django.core.cache  import cache
BALANCE_OUTSIDE_LIST = ['BTC', 'QTUM', 'BCH', 'ADA', 'TRX']

class ColdwalletBalanceUpdate(APIView):
    name = "cold_wallet_balance_update"

    permission_classes = [ColdwalletBalanceUpdatePermission]

    def post(self, request, *args, **kwargs):

        coin = request.data.get('coin', None).upper()
        address = request.data.get('address', None)
        cold_balance = request.data.get('balance', None)

        manager = CoinManager()
        if coin not in BALANCE_OUTSIDE_LIST:
            if address is None:
                return Response(data="Address is needed",status=status.HTTP_400_BAD_REQUEST)

            cold_balance = manager.getCoinBalance2(coin, address)

        if cold_balance is not None:
            cache.set("bcg:coldwallet:balance:" + coin, cold_balance, timeout=None)

        hot_balance = manager.getCoinBalance2(coin)
        if hot_balance is not None:
            cache.set("bcg:hotwallet:balance:" + coin, hot_balance, timeout=None)

        cache.close()

        return Response(status=status.HTTP_200_OK)