from . import *

class DepositAddressRetrieveDestroy(RetrieveDestroyAPIView):
    """
    입금주소 조회 및 삭제
    """
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "deposit-address-retrieve-destory"
    permission_classes = [DepositAddressRetrieveDestroyPermission]
    serializer_class = DepositAddressSerializer
    queryset = DepositAddress.objects.all()