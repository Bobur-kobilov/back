from . import *


# 체결내역 query
def done_query(self):
    query = """
        SELECT 
            t.id 				    AS id
            , bid.ask    			AS bid_ask
            , bid.bid    			AS bid_bid
            , ask.bid    			AS ask_bid
            , ask.ask    			AS ask_ask
            , t.currency            AS trd_currency
            , t.price    			AS trd_price
            , t.volume   			AS trd_volume
            , t.funds    			AS trd_funds
            , t.trend    			AS trd_trend
            , t.created_at   		AS trd_created_at
            , bid.id     			AS bid_id
            , bid.member_id  		AS bid_member_id
            , bid.price  			AS bid_price
            , bid.origin_volume  	AS bid_origin_volume
            , t.bid_fee  			AS trd_bid_fee
            , bid.created_at     	AS bid_created_at
            , ask.id     			AS ask_id
            , ask.member_id  		AS ask_member_id
            , ask.price  			AS ask_price
            , ask.origin_volume  	AS ask_origin_volume
            , t.ask_fee  			AS trd_ask_fee
            , ask.created_at     	AS ask_created_at
        FROM
            trades t
        INNER JOIN
            orders bid ON t.bid_id = bid.id
        INNER JOIN
            orders ask ON t.ask_id = ask.id
    """
    return query


# 체결내역 조회
class OrderDoneList(RawQueryListAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "order-done-list"
    permission_classes = [OrderDonePermission]
    #--------------------------------------
    #  PROPERTIES : FILTER
    #--------------------------------------
    having_fields   = []
    filter_fields   = []
    search_fields   = []
    ordering_fields = ['trd_created_at']
    ordering        = ['-trd_created_at']
    pagination_class = RawQuerySetPagination
    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = TradesSerializer
        return serializer

    def add_filter(self, query = None, member_id = None, start = None, end = None, order_number = None, trade_id = None, market = None):
        # 거래소 회원검색
        if member_id is not None:
            query = RawQuerySyntax.add_where(query, "(bid.member_id = {0} OR ask.member_id = {0})".format(int(member_id)))

        # 날짜 검색 (UTC 시간으로 변경 후 쿼리 실행)
        if start is not None and start is not '' and str(start) != 'Invalid date' and end is not None and end is not '' and str(end) != 'Invalid date':
            start_date = set_time_zone(start, timezone('UTC'), 'start')
            end_date = set_time_zone(end, timezone('UTC'), 'end')
            query = RawQuerySyntax.add_where( query, "t.created_at BETWEEN '{0}' AND '{1}'".format(start_date, end_date))

        # 주문번호 검색
        if order_number is not None and order_number is not '':
            query = RawQuerySyntax.add_where( query, "(bid.id = ({0}) OR ask.id = ({0}))".format(order_number))

        # 체결번호 검색
        if trade_id is not None and trade_id is not '':
            query = RawQuerySyntax.add_where( query, "t.id = {0}".format(trade_id))

        # 마켓 검색
        if market is not None and market is not '' and market != 'all':
            market = market.split(',')
            # 값이 id값이 아닌 'BTC/EHT' 등 문자값으로 들어오기 때문에 값 변경
            for i in range(len(market)):
                market[i] = selectMarketDic[market[i]]['code']
            query = RawQuerySyntax.add_where( query, "t.currency IN ({0})".format(str(list(market))[1:-1]))

        return query

    # 응답하기
    def list(self, request):

        query = done_query(self)

        # 주문번호 조회
        order_number    = request.GET.get('id'              , None)

        # 체결번호 검색
        trade_id        = request.GET.get('trade_id'        , None)

        # 조회기간선택
        start_date      = request.GET.get('start_date'      , None)
        end_date        = request.GET.get('end_date'        , None)

        # 엑셀 여부
        is_excel = bool(request.query_params.get('excel', False))

        # 주문번호, 체결번호로 조회시 기간 설정 불필요
        if order_number is None and trade_id is None:
            if start_date is None or end_date is None:
                return Response (
                    # "조회기간을 선택해주세요."
                    data    = ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00013)
                    , status = status.HTTP_404_NOT_FOUND
                )

        # 회원정보로 검색
        member_id       = request.query_params.get('member_id', None)

        # 마켓 검색
        market          = request.GET.get('market'          , None)

        query = self.add_filter(
            query           = query
            , start         = start_date
            , end           = end_date
            , member_id     = member_id
            , order_number  = order_number
            , trade_id      = trade_id
            , market        = market
        )

        if query is None:
            return Response (
                # "일치하는 값이 없습니다."
                data    = ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00008)
                , status = status.HTTP_404_NOT_FOUND
            )

        queryset = self.get_queryset(model=Trades, query=query, __db__ = 'exchange')

        pagination = self.pagination_class()
        serializer = self.get_serializer_class()( queryset, many=True)
        if not is_excel:
            queryset = pagination.paginate_queryset(queryset, request, __db__ = 'exchange')

        # 가져온 UTC시간을 local 시간으로 변경
        for obj in serializer.data:
            for str in obj:
                if str.find("created_at") > -1 and obj[str] is not None:
                    utc_time = datetime.strptime((obj[str]), "%Y-%m-%d %H:%M:%S").replace(tzinfo=pytz.UTC)
                    obj[str] = utc_time.astimezone(timezone(settings.TIME_ZONE)).strftime("%Y-%m-%d %H:%M:%S")

        if not is_excel:
            return pagination.get_paginated_response(serializer.data)
        else:
            return Response({'results': serializer.data})

    # utc 시간을 local시간으로 환산하는 기능
    def utcToLocal(self, time = None):
        if time is not None:
            time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S").replace(tzinfo=pytz.UTC)
            time = time.astimezone(timezone(settings.TIME_ZONE)).strftime("%Y-%m-%d %H:%M:%S")
        return time