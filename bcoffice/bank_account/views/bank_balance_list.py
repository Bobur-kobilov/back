from . import *

# KRW 잔고조회
class BankBalanceList(ListAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "bank-balance-list"
    permission_classes = [BankBalanceListPermission]
    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = BankBalanceSerializer
        return serializer
    
    # 쿼리셋 가져오기
    def get_queryset(self):
        return Accounts.objects.using('exchange').values('currency').annotate(balance_total=Sum('balance'), locked_total=Sum('locked')).filter(currency=1)