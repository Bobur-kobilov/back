from . import *

# 암호화폐 입금내역조회 query
def deposit_query(self):
    query = '''
        SELECT 
            d.id				AS id
            , d.account_id		AS account_id
            , d.member_id		AS member_id
            , d.currency		AS currency
            , d.amount			AS amount
            , d.fee				AS fee
            , d.fund_uid		AS fund_uid
            , d.fund_extra		AS fund_extra
            , d.txid			AS txid
            , d.state			AS state
            , d.aasm_state		AS aasm_state
            , d.created_at		AS created_at
            , d.updated_at		AS updated_at
            , d.done_at			AS done_at
            , d.confirmations	AS confirmations
            , d.type			AS type
            , d.payment_transaction_id	AS payment_transaction_id
            , d.txout			AS txout
            , p.address			AS address
        FROM
            deposits d
        LEFT OUTER JOIN
            payment_transactions p
        ON
            d.payment_transaction_id = p.id
    '''
    return query


# 암호화폐 입금내역조회
class CoinDepositHistoryList(RawQueryListAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "coin-deposits-history-list"
    permission_classes = [CoinDepositHistoryPermission]
    #--------------------------------------
    #  PROPERTIES : FILTER
    #--------------------------------------
    having_fields       = []
    filter_fields       = []
    search_fields       = []
    ordering_fields     = ['created_at']
    ordering            = ['-created_at']
    pagination_class    = RawQuerySetPagination
    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = CoinDepositHistorySerializer
        return serializer

    def add_filter(self, query = None, member_id = None, start_date = None, end_date = None, aasm_state = None, currency = None, deposit_id = None, txid = None, address = None):
        # 회원정보로 검색
        if member_id is not None:
            query = RawQuerySyntax.add_where(query, "d.member_id = {0}".format(int(member_id)))

        # 날짜 검색
        if start_date is not None and start_date is not '' and str(start_date) != 'Invalid date':
            start_date = set_time_zone(start_date, timezone('UTC'), 'start')
            query = RawQuerySyntax.add_where(query, "d.created_at >= '{0}'".format(start_date))
        if end_date is not None and end_date is not '' and str(end_date) != 'Invalid date':
            end_date = set_time_zone(end_date, timezone('UTC'), 'end')
            query = RawQuerySyntax.add_where(query, "d.created_at <= '{0}'".format(end_date))

        # 거래상태 조회
        if aasm_state is not None and aasm_state is not '' and aasm_state != 'all':
            aasm_state  = aasm_state.split(',')
            query       = RawQuerySyntax.add_where(query, "d.aasm_state IN ({0})".format(str(list(aasm_state))[1:-1]))

        # 암호화폐 조회
        if currency is not None and currency is not '' and currency != 'all':
            currency    = currency.split(',')
            query       = RawQuerySyntax.add_where(query, "d.currency IN ({0})".format(str(list(currency))[1:-1]))

        # 입금번호 조회
        if deposit_id is not None and deposit_id is not '':
            query       = RawQuerySyntax.add_where(query, "d.id = {0}".format(deposit_id))

        # TXID 조회
        if txid is not None and txid is not '':
            query       = RawQuerySyntax.add_where(query, "d.txid = '{0}'".format(txid))

        # 입금주소 조회
        if address is not None and address is not '':
            query       = RawQuerySyntax.add_where(query, "p.address = '{0}'".format(address))

        return query

    def list(self, request, *args, **kwargs):

        query = deposit_query(self)

        # 조회기간선택
        start_date      = request.GET.get('start_date')
        end_date        = request.GET.get('end_date')

        # 거래소 이용자 필터링
        member_id       = request.query_params.get('member_id', None)

        # 상태 조회
        aasm_state      = request.GET.get('aasm_state'  , None)

        # 암화화폐 조회
        currency        = request.GET.get('currency'    , None)

        # 주문번호 조회
        deposit_id      = request.GET.get('id'          , None)

        # TXID 조회
        txid            = request.query_params.get('txid', None)

        # 입금주소 조회
        address         = request.query_params.get('address', None)

        # 엑셀 여부
        is_excel = bool(request.query_params.get('excel', False))

        query = self.add_filter(
            query           = query
            , member_id     = member_id
            , start_date    = start_date
            , end_date      = end_date
            , aasm_state    = aasm_state
            , currency      = currency
            , deposit_id    = deposit_id
            , txid          = txid
            , address       = address
        )

        queryset = self.get_queryset(model=Deposits, query=query, __db__ = 'exchange')#self.filter_queryset(self.get_queryset())

        # Pagination 클래스의 인스턴스를 생성한다
        pagination = self.pagination_class()

        # 쿼리셋을 시리얼라이징 한다.
        serializer = self.get_serializer_class()( queryset, many=True)

        if not is_excel:
            queryset = pagination.paginate_queryset(queryset, request, __db__ = 'exchange')
            return pagination.get_paginated_response( serializer.data )
        else:
            return Response({'results': serializer.data})