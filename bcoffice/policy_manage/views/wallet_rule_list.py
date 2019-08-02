from . import *

class WalletRuleList(ListAPIView):
    """
    지갑규칙 목록 가져오기
    """
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "wallet-rule-list"
    permission_classes = [WalletRuleListPermission]
    serializer_class = WalletRuleSerializer
    queryset = WalletRule.objects.all()
    ordering = ['currency']

    #--------------------------------------
    #  METHODS
    #--------------------------------------
    def get(self, request, *args, **kwargs):
        """
        설정된 코인의 규칙정보가 없을 경우
        리스트를 가져오는 것 이전에 선행적으로 기본 규칙을 INSERT하는 과정을 거친다.
        이 과정에서 설정된 코인에는 없지만 규칙에 코인이 존재하는 경우
        해당 코인은 삭제하는 과정을 진행한다.
        """
        currency_list = settings.CURRENCY_LIST
        wallet_list = list( WalletRule.objects.all() )
        delete_list = []

        """
        삭제과정. 지갑 목록의 아이템이 currency_list에 존재하는지 여부를 파악한 뒤
        delete_list 객체에 append를 한다.
        """
        for wallet in wallet_list:
            result = False

            for item in currency_list:
                if item['id'] == wallet.currency:
                    result = True
                    break

            if result is False:
                delete_list.append(wallet)

        """
        delete_list에 들어있는 WalletRule 인스턴스객체를 모두 삭제한다.
        """
        for item in delete_list:
            item.delete()

        """
        currency_list와 wallet_list를 비교해 추가가 필요한 코인을 추가한다.
        """
        for item in currency_list:
            result = False

            for wallet in wallet_list:
                if item['id'] == wallet.currency:
                    result = True
                    break

            if result is False:
                instance = WalletRule(
                    currency = item['id']
                    , target_rate = 10
                )

                instance.save()


        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)

        result = serializer.data

        hot_wallet = []
        cold_wallet = []

        hot_list = DepositAddress.objects.filter(wallet_type='HOT')
        cold_list = DepositAddress.objects.filter(wallet_type = 'COLD')

        if cold_list.exists() is True :
            cold_list = list(cold_list)
        else :
            cold_list = []

        for item in settings.CURRENCY_LIST:
            if item['code'] == "krw":
                continue

            hot_balance = 0 # cache.get("bcg:hotwallet:" + item['code'] + ":balance" )
            cold_balance = 0.0

            for hot_item in hot_list:
                if hot_item.currency == item['id']:
                    manager = CoinManager()
                    hot_balance = float(manager.getCoinBalance(item['code'])['result'])

            if hot_balance is None:
                hot_balance = 0

            hot_wallet.append({
                'currency': item['id']
                , 'balance': hot_balance
            })

            for cold_item in cold_list:
                if cold_item.currency == item['id'] :
                    get_path = "bcg:coldwallet:balance:" + item['code'].upper() + ":" + cold_item.address
                    # cold_balance += cache.get(get_path)
                    balance = cache.get(get_path)
                    if balance is not None:                        
                        cold_balance += float(balance)

            cold_wallet.append({
                'currency': item['id']
                , 'balance': cold_balance
            })

        for item in result:
            for hot_item in hot_wallet:
                if item['currency'] == hot_item['currency']:
                    item['hot'] = hot_item['balance']
                    break

            for cold_item in cold_wallet:
                if item['currency'] == cold_item['currency']:
                    item['cold'] = cold_item['balance']
                    break

        return Response(result)