from . import *

class DepositAddressList(ListAPIView):
    """
    입금주소 목록 가져오기
    """
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "deposit-address-create"
    permission_classes = [DepositAddressListPermission]
    serializer_class = DepositAddressSerializer
    pagination_class = LimitOffsetPagination
    ordering = ['-id']
    #--------------------------------------
    #  METHODS
    #--------------------------------------
    def get_queryset(self):
        queryset = DepositAddress.objects

        emp_no          = self.request.query_params.get("emp_no"        , None)
        start_date      = self.request.query_params.get("start_date"    , None)
        end_date        = self.request.query_params.get("end_date"      , None)
        currency        = self.request.query_params.get("currency"      , None)
        address_type    = self.request.query_params.get("address_type"  , None)

        if emp_no is not None:
            queryset = queryset.filter(author__emp_no = emp_no)

        if start_date is not None:
            start_date += " 00:00:00"
            queryset = queryset.filter(created_at__gte = start_date)

        if end_date is not None:
            end_date += " 23:59:59"
            queryset = queryset.filter(created_at__lte = end_date)

        if currency is not None:
            queryset = queryset.filter(currency = currency)

        if address_type is not None:
            queryset = queryset.filter(address_type = address_type)

        return queryset