from django.conf    import settings
from .api_service   import APIService
import json

class CoinManager:
    def __init__(self):
        pass

    def transCurrencyIdToName(self, currency):
        coin_name = None

        if isinstance( currency, str ) :
            currency = int( currency )

        for item in settings.CURRENCY_LIST:
            if currency == item['id']:
                coin_name = item['code']
                break
        
        return coin_name


    def getCoinBlockHeight(self, coin, *args, **kwargs) :
        coin_manager_host = settings.COIN_MANAGER_ADDRESS
        address = '/coin'
        params = {}
        params['coin'] = coin
        params['method'] = 'getblockstate'

        data = APIService.rpc_call(url = coin_manager_host + address, params=params, method='post', timeout=5)
        
        return data

    def getCoinBalance(self, coin, addr=None):
        coin_manager_host = settings.COIN_MANAGER_ADDRESS
        address = '/coin'
        params = {}
        params['coin'] = coin
        params['method'] = 'getbalance'

        if addr:
            params['params'] = [addr]

        data = APIService.rpc_call(url = coin_manager_host + address, params=params, method='post', is_json=True)

        return data

    def getCoinBalance2(self, coin, addr=None):
        coin_manager_host = settings.COIN_MANAGER_ADDRESS
        address = '/coin'
        params = {}
        params['coin'] = coin
        params['method'] = 'getbalance'

        if addr:
            params['params'] = [addr]

        data = APIService.rpc_call(url = coin_manager_host + address, params=params, method='post', is_json=True)
        if data['error'] is not None:
            return None
        return float(data['result'])

    def sendToAddress(self, coin, *args, **kwargs) :
        address = kwargs.get('address', None)
        amount = kwargs.get('amount', None)

        if address is None :
            raise ValueError('The variable "address" is required.')
        
        if amount is None :
            raise ValueError('The variable "amount" is required.')

        coin_manager_host = settings.COIN_MANAGER_ADDRESS
        path = '/coin'
        params = {}
        params['coin'] = coin
        params['method'] = 'sendtoaddress'
        params['params'] = [
            address, amount
        ]

        data = APIService.rpc_call(url = coin_manager_host + path, params=params, method='post', is_json=True)
        
        return data
