from . import *


# 암호화폐 출금내역조회
class CoinWithdrawHistoryList(ListAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "coin-withdraw-history-list"
    permission_classes = [CoinWithdrawHistoryPermission]
    #--------------------------------------
    #  PROPERTIES : FILTER
    #--------------------------------------
    filter_fields       = ['id']
    search_fields       = []
    ordering_fields     = ['created_at']
    ordering            = ['-created_at']
    pagination_class    = StandardPagination
    page_size_query_param = ""
    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = CoinWithdrawHistorySerializer
        return serializer

    # 쿼리셋 가져오기
    def get_queryset(self, order_id = None, start = None, end = None, member_id = None, aasm_state = None, currency = None, txid = None, withdraw_address = None):

        query           = Withdraws.objects.using("exchange")
        # 주문번호 검색
        if order_id is not None and order_id is not '':
            query = query.filter(id = order_id)

        # 회원검색
        if member_id is not None:
            query = query.filter(member_id = int(member_id))

        # 조회시간 설정
        if start is not None and start is not '' and str(start) != 'Invalid date':
            start_date  = start + ' 00:00:00'
            query       = query.filter(created_at__gte = start_date)
        if end is not None and end is not '' and str(end) != 'Invalid date':
            end_date    = end + ' 23:59:59'
            query       = query.filter(created_at__lte = end_date)

        # 거래상태 조회
        if aasm_state is not None and aasm_state is not '' and aasm_state != 'all':
            aasm_state  = aasm_state.split(',')
            query       = query.filter(aasm_state__in = aasm_state)

        # 암호화폐 조회
        if currency is not None and currency is not '' and currency != 'all':
            currency    = currency.split(',')
            query       = query.filter(currency__in = currency)

        if txid is not None and txid is not '':
            query       = query.filter(txid = txid)

        if withdraw_address is not None and withdraw_address is not '':
            query = query.filter(fund_uid=withdraw_address)
    
        return query

    # email 추가
    def list(self, request, *args, **kwargs):
        # 주문번호 조회
        order_id = request.GET.get('id', None)

        # 조회기간선택
        start_date = request.GET.get('start_date',None)
        end_date = request.GET.get('end_date', None)

        # 거래소 이용자 필터링
        member_id = request.query_params.get('member_id', None)

        # 상태 조회
        aasm_state = request.GET.get('aasm_state', None)

        # 암호화폐 조회
        currency = request.GET.get('currency', None)

        # TXID 조회
        txid = request.query_params.get('txid',None)

        withdraw_address = request.query_params.get('withdraw_address', None)

        # 엑셀 여부
        is_excel = bool(request.query_params.get('excel',False))

        queryset = self.get_queryset(
            order_id        = order_id
            , start         = start_date
            , end           = end_date
            , member_id     = member_id
            , aasm_state    = aasm_state
            , currency      = currency
            , txid          = txid
            , withdraw_address = withdraw_address
        )

        if queryset is None:
            return Response (
                    # "일치하는 값이 없습니다."
                    data    = ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00008)
                    ,status = status.HTTP_404_NOT_FOUND
                )

        queryset = self.filter_queryset(queryset)

        if not is_excel:
            queryset = self.paginate_queryset(queryset)

        serializer = self.get_serializer(queryset, many=True)

        if not is_excel:
            return self.get_paginated_response(serializer.data)
        else:
            return Response({'results': serializer.data})