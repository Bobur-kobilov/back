from . import *

# 암호화폐 출금내역상세조회
class CoinWithdrawHistoryDetail(RetrieveAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "coin-withdraw-history-detail"
    permission_classes = [CoinWithdrawHistoryDetailPermission]
    #--------------------------------------
    #  PROPERTIES : FILTER
    #--------------------------------------
    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = CoinWithdrawHistorySerializer
        return serializer

    # 쿼리셋 가져오기
    def get_queryset(self):
        return Withdraws.objects.using('exchange')