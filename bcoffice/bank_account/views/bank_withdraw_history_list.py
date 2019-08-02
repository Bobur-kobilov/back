from . import *

# KRW 출금내역조회
class BankWithdrawHistoryList(ListAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "bank-withdraw-history-list"
    permission_classes = [BankWithdrawHistoryListPermission]
    pagination_class = StandardPagination
    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = BankWithdrawHistorySerializer
        return serializer
    
    # 쿼리셋 가져오기
    def get_queryset(self):
        return Withdraws.objects.using("exchange").all().filter(currency=1)

    # email 추가
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        serializer = self.get_serializer(page, many=True)
    
        for obj in serializer.data:
            obj['member_email'] = Members.objects.using('exchange').values_list('email', flat=True).filter(id=obj['member_id'])
        
        return self.get_paginated_response(serializer.data)