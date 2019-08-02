from . import *

BALANCE_OUTSIDE_LIST = ['BTC', 'QTUM', 'BCH', 'ADA', 'TRX']

# 암호화폐 잔고조회
class CoinBalanceList(ListAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "coin-balance-list"
    permission_classes = [CoinBalancePermission]
    #--------------------------------------
    #  PROPERTIES : FILTER
    #--------------------------------------
    filter_fields   = []
    search_fields   = []
    ordering_fields = ['currency']
    ordering        = ['currency']



    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = CoinBalanceSerializer
        return serializer

    # 쿼리셋 가져오기
    def get_queryset(self):
        return Accounts.objects.using('exchange').values('currency').annotate(balance_total=Sum('balance'), locked_total=Sum('locked'))

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        result = {}
        walletRule = list(WalletRule.objects.all())
        hot_list = DepositAddress.objects.filter(wallet_type='HOT')
        cold_list = DepositAddress.objects.filter(wallet_type='COLD')
        
        # https://stackoverflow.com/questions/1387727/checking-for-empty-queryset-in-django
        # if hot_list.exists() is True :
        if hot_list:
            hot_list = list(hot_list)
        else:
            hot_list = []

        # if cold_list.exists() is True :
        if cold_list:
            cold_list = list(cold_list)
        else:
            cold_list = []

        ledger_data = serializer.data

        result = []
        for item in settings.CURRENCY_LIST:
            coin_code = item['code']
            coin_id = item['id']
        
            if coin_code == "krw":
                continue

            hot_balance = 0.0
            cold_balance= 0.0

            # Hot wallet
            rule_item = WalletRule.findByCurrency(walletRule, coin_id)

            get_path = "bcg:hotwallet:balance:" + coin_code.upper()
            hot_balance = cache.get(get_path)
            if hot_balance is None:
                hot_balance = 0

            # Cold wallet
            cold_item = next((cold_item for cold_item in cold_list if cold_item.currency == coin_id), None)
            if cold_item:
                get_path = "bcg:coldwallet:balance:" + coin_code.upper()
                balance = cache.get(get_path)

                if balance is not None:
                    cold_balance += float(balance)

            ledger_item = next((ledger_item for ledger_item in ledger_data if ledger_item['currency'] == coin_id), None)
            if ledger_item:
                ledger_tot_balance = ledger_item['balance_total'] + ledger_item['locked_total']
            else:
                ledger_tot_balance = -1

            wallet_tot_balance = hot_balance + cold_balance

            data = {
                  'code': coin_code
                , 'id': coin_id
                , 'ledger_tot_usd': ValuationAssetsUtil.get_valuation_for_dollar(coin_id, ledger_tot_balance)
                , 'wallet_tot_usd': ValuationAssetsUtil.get_valuation_for_dollar(coin_id, wallet_tot_balance)
                , 'ledger_tot_balance': ledger_tot_balance
                , 'wallet_tot_balance': wallet_tot_balance

                , 'hotwallet': hot_balance
                , 'hot_usd': ValuationAssetsUtil.get_valuation_for_dollar(coin_id, hot_balance)
                , 'hot_rate': rule_item.target_rate if rule_item else ''

                , 'coldwallet': cold_balance
                , 'cold_rate': 100 - rule_item.target_rate if rule_item else ''
                , 'cold_usd':  ValuationAssetsUtil.get_valuation_for_dollar(coin_id, cold_balance)

                , 'cold_wallet_addr': cold_item.address if cold_item else ''
                , 'is_cold_update': coin_code.upper() in BALANCE_OUTSIDE_LIST
            }

            result.append(data)

        return Response(result)