from django.conf import settings
from api_service import APIService
import config


class CoinManager:
    def __init__(self):
        pass

    def getCoinBlance(self, coin, addr=None):
        coin_manager_host = config.COIN_MANAGER_ADDRESS
        address = '/coin'
        params = {}
        params['coin'] = coin
        params['method'] = 'getbalance'

        if address:
            params['params'] = [addr]


        data = APIService.rpc_call(url=coin_manager_host + address, params=params, method='post', is_json=True)

        return data