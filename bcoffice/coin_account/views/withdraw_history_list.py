from . import *

class WithdrawHistoryList(ListAPIView):
    """
    출금내역 목록
    """
    name = "withdraw_history"
    permission_classes  = [WithdrawHistoryListPermission]
    pagination_class    = LimitOffsetPagination

    def get_serializer_class(self):
        serializer = WithdrawHistorySerializer
        return serializer

    def get_queryset(self, *args, **kwargs):
        queryset = WithdrawHistory.objects.all()

        requester       = kwargs.get('requester', None)
        start_date      = kwargs.get('start_date', None)
        end_date        = kwargs.get('end_date', None)
        wallet_type     = kwargs.get('wallet_type', None)
        currency        = kwargs.get("currency", None)
        withdraw_number = kwargs.get("withdraw_number", None)

        if requester is not None :
            queryset = queryset.filter(requester__emp_no = requester)

        if start_date is not None :
            start_date += " 00:00:00"
            queryset = queryset.filter(created_at__gte = start_date)

        if end_date is not None :
            end_date += " 23:59:59"
            queryset = queryset.filter(created_at__lte = end_date)

        if currency is not None :
            queryset = queryset.filter(currency = currency)

        if wallet_type is not None :
            queryset = queryset.filter(wallet__wallet_type = wallet_type)

        if withdraw_number is not None :
            queryset = queryset.filter(id = withdraw_number)

        return queryset.order_by("-created_at")

    def list(self, request, *args, **kwargs):
        requester       = request.query_params.get('requester', None)
        start_date      = request.query_params.get('start_date', None)
        end_date        = request.query_params.get('end_date', None)
        wallet_type     = request.query_params.get('wallet_type', None)
        currency        = request.query_params.get("currency", None)
        withdraw_number = request.query_params.get("withdraw_number", None)
        # 엑셀 여부
        is_excel = bool(request.query_params.get('excel', False))

        queryset = self.get_queryset(
            requester           = requester
            , start_date        = start_date
            , end_date          = end_date
            , wallet_type       = wallet_type
            , currency          = currency
            , withdraw_number   = withdraw_number
        )

        if not is_excel:
            queryset = self.paginate_queryset(queryset)

        serializer = self.get_serializer(queryset, many=True)

        if not is_excel:
            return self.get_paginated_response(serializer.data)
        else:
            return Response({'results': serializer.data})