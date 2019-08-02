from . import *

class WalletRuleUpdate(UpdateAPIView):
    """
    지갑규칙 수정
    """
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "wallet-rule-update"
    permission_classes = [WalletRuleListPermission]
    serializer_class = WalletRuleSerializer
    queryset = WalletRule.objects.all()