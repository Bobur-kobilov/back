from api_service import APIService


class CoinManager:
    def __init__(self, coin_manager_host):
        self.coin_manager_host = coin_manager_host
        
    def getCoinBalance(self, coin, *args, **kwargs):        
        address = '/coin'
        params = {}
        params['coin'] = coin
        params['method'] = 'getbalance'

        data = APIService.rpc_call(url=self.coin_manager_host + address, params=params, method='post', is_json=True)

        return data