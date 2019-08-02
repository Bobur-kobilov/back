from . import *

# 상세주문내역 query
def order_detail_query(self, type = None):
    query = ''
    if(type == 'bid'):
        query = """
            SELECT
                o.id                AS id,
                o.member_id         AS o_member_id,
                o.origin_id         AS o_origin_id,
                o.first_id          AS o_first_id,
                t1.id               AS t_id,
                o.state             AS o_state,
                o.type              AS o_type,
                o.bid               AS o_bid,
                o.ask               AS o_ask,
                o.currency          AS o_currency,
                o.ord_type          AS o_ord_type,
                o.source            AS o_source,
                o.origin_volume     AS o_origin_volume,
                o.volume            AS o_volume,
                o.price             AS o_price,
                s.price             AS s_price,
                o.locked            AS o_locked,
                o.origin_locked     AS o_origin_locked,
                t1.bid_id           AS t_bid_id,
                t1.ask_id           AS t_ask_id,
                t1.price            AS t_price,
                t1.volume           AS t_volume,
                (select o.origin_volume - sum(volume) from trades where bid_id = o.id and id <= t1.id) as t_remain_volume,
                t1.funds            AS t_funds,
                t1.bid_fee          AS t_bid_fee,
                t1.ask_fee          AS t_ask_fee,
                s.created_at        AS s_created_at,
                o.created_at        AS o_created_at,
                t1.created_at       AS t_created_at
            FROM
                orders o
            LEFT OUTER JOIN
                trades t1 ON o.id = t1.bid_id
            LEFT OUTER JOIN
                stop_orders s ON o.id = s.order_id
            WHERE if(o.state = 200 AND o.type NOT LIKE CONCAT('Cac','%%'), t1.id, o.id) is not null
        """
    elif(type == 'ask'):
        query = """
            SELECT
                o.id                AS id,
                o.member_id         AS o_member_id,
                o.origin_id         AS o_origin_id,
                o.first_id          AS o_first_id,
                t1.id               AS t_id,
                o.state             AS o_state,
                o.type              AS o_type,
                o.bid               AS o_bid,
                o.ask               AS o_ask,
                o.currency          AS o_currency,
                o.ord_type          AS o_ord_type,
                o.source            AS o_source,
                o.origin_volume     AS o_origin_volume,
                o.volume            AS o_volume,
                o.price             AS o_price,
                s.price             AS s_price,
                o.locked            AS o_locked,
                o.origin_locked     AS o_origin_locked,
                t1.bid_id           AS t_bid_id,
                t1.ask_id           AS t_ask_id,
                t1.price            AS t_price,
                t1.volume           AS t_volume,
                (select o.origin_volume - sum(volume) from trades where ask_id = o.id and id <= t1.id) as t_remain_volume,
                t1.funds            AS t_funds,
                t1.bid_fee          AS t_bid_fee,
                t1.ask_fee          AS t_ask_fee,
                s.created_at        AS s_created_at,
                o.created_at        AS o_created_at,
                t1.created_at       AS t_created_at
            FROM
                orders o
            LEFT OUTER JOIN
                trades t1 ON o.id = t1.ask_id
            LEFT OUTER JOIN
                stop_orders s ON o.id = s.order_id
            WHERE if(o.state = 200 AND o.type NOT LIKE CONCAT('Cac','%%'), t1.id, o.id) is not null
        """
    return query


# 상세주문내역 조회
class OrderDetailList(RawQueryListAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "order-detail-list"
    permission_classes = [OrderDetailPermission]
    #--------------------------------------
    #  PROPERTIES : FILTER
    #--------------------------------------
    having_fields       = []
    filter_fields       = []
    search_fields       = []
    ordering_fields     = []
    ordering            = []
    pagination_class    = RawQuerySetPagination
    page_size_query_param = ""
    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = OrderDetailSerializer
        return serializer

    def add_filter(self, query_bid = None, query_ask = None, member_id = None, order_number = None, ord_type = None, market = None, start_date = None, end_date = None):

        # 거래소 회원검색
        if member_id is not None:
            query_bid = RawQuerySyntax.add_where(query_bid, "o.member_id = {0}".format(int(member_id)))
            query_ask = RawQuerySyntax.add_where(query_ask, "o.member_id = {0}".format(int(member_id)))

        # 날짜 검색 (UTC 시간으로 변경 후 쿼리실행)
        if start_date is not None and start_date is not '' and str(start_date) != 'Invalid date' and end_date is not None and end_date is not '' and str(end_date) != 'Invalid date':
            start_date = set_time_zone(start_date, timezone('UTC'), 'start')
            end_date = set_time_zone(end_date, timezone('UTC'), 'end')

            query_bid = RawQuerySyntax.add_where(query_bid, "o.created_at BETWEEN '{0}' AND '{1}'".format(start_date, end_date))
            query_ask = RawQuerySyntax.add_where(query_ask, "o.created_at BETWEEN '{0}' AND '{1}'".format(start_date, end_date))

        # 주문번호 검색
        if order_number is not None and order_number is not '':
            query_bid = RawQuerySyntax.add_where(query_bid, "o.id = {0}".format(order_number))
            query_ask = RawQuerySyntax.add_where( query_ask, "o.id = {0}".format(order_number))

        # 주문유형 검색
        if ord_type is not None and ord_type is not '':
            query_bid = RawQuerySyntax.add_where( query_bid, "o.ord_type = '{0}'".format(ord_type))
            query_ask = RawQuerySyntax.add_where( query_ask, "o.ord_type = '{0}'".format(ord_type))

        # 마켓 검색
        if market is not None and market is not '' and market != 'all':
            market = market.split(',')
            # 값이 id값이 아닌 'BTC/EHT' 등 문자값으로 들어오기 때문에 값 변경
            for i in range(len(market)):
                market[i] = selectMarketDic[market[i]]['code']
            query_bid = RawQuerySyntax.add_where( query_bid, "o.currency IN ({0})".format(str(list(market))[1:-1]))
            query_ask = RawQuerySyntax.add_where( query_ask, "o.currency IN ({0})".format(str(list(market))[1:-1]))

        query = '(' + query_bid + ') UNION (' + query_ask + ')'
        return query

    # 응답하기
    def list(self, request):

        query_bid = order_detail_query(self, 'bid')
        query_ask = order_detail_query(self, 'ask')

        # 주문번호 조회
        order_number        = request.GET.get('id'    , None)

        # 조회기간선택
        start_date          = request.GET.get('start_date'  , None)
        end_date            = request.GET.get('end_date'    , None)

        # 주문번호로 바로 조회 할 경우가 생기기 때문에 주문번호가 없을때만 조회기간 제한
        if order_number is None:
            if start_date is None or end_date is None:
                return Response (
                    # "조회기간을 선택해주세요."
                    data    = ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00013)
                    , status = status.HTTP_404_NOT_FOUND
                )

        # 회원정보 조회
        member_id           = request.query_params.get('member_id', None)

        # 주문유형 조회
        ord_type            = request.GET.get('ord_type'    , None)

        # 마켓 검색
        market              = request.GET.get('market'      , None)

        # 엑셀 여부
        is_excel = bool(request.query_params.get('excel', False))

        query = self.add_filter (
            query_bid       = query_bid
            , query_ask     = query_ask
            , member_id     = member_id
            , order_number  = order_number
            , ord_type      = ord_type
            , market        = market
            , start_date    = start_date
            , end_date      = end_date
        )

        if query is None:
            return Response (
                # "일치하는 값이 없습니다."
                data    = ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00008)
                , status = status.HTTP_404_NOT_FOUND
            )

        queryset = self.get_queryset(model=Orders, query=query, __db__ = 'exchange')#self.filter_queryset(self.get_queryset())

        # 정렬하기
        ordering            = request.GET.get('ordering'    , None)

        queryset = self.add_ordering (
            queryset = queryset
            , ordering = ordering
        )
        # Pagination 클래스의 인스턴스를 생성한다
        pagination = self.pagination_class()

        # 쿼리셋을 시리얼라이징 한다.
        serializer = self.get_serializer_class()( queryset, many=True)

        # count_query : raw query에서 select ~ from 사이에
        # 서브쿼리 발생할 경우 count하는 쿼리를 작성하여 사용
        count_query = queryset.query.__str__()

        # ORDER BY 분리
        split_before_order = count_query.split(') ORDER BY')[0]

        # UNION 분리 후 COUNT 처리
        split_before_union = split_before_order.split(') UNION (')[0]
        split_before_union = 'SELECT o.id as o_id, t1.id as t_id FROM' + split_before_union.split('FROM')[1]

        split_after_union = split_before_order.split(') UNION (')[1]
        split_after_union = 'SELECT o.id as o_id, t1.id as t_id FROM' + split_after_union.split('FROM')[1]

        count_query = "SELECT count(*) as count FROM ((" + split_before_union + ") UNION (" + split_after_union + ")) count"

        if not is_excel:
            queryset = pagination.paginate_queryset(queryset, request, __db__ = 'exchange', count_query = count_query)

        # 가져온 UTC시간을 local 시간으로 변경
        for obj in serializer.data:
            for str in obj:
                if str.find("created_at") > -1 and obj[str] is not None:
                    utc_time = datetime.strptime((obj[str]), "%Y-%m-%d %H:%M:%S").replace(tzinfo=pytz.UTC)
                    obj[str] = utc_time.astimezone(timezone(settings.TIME_ZONE)).strftime("%Y-%m-%d %H:%M:%S")

        if not is_excel:
            return pagination.get_paginated_response( serializer.data )
        else:
            return Response({'results': serializer.data})

    # utc 시간을 local시간으로 환산하는 기능
    def utcToLocal(self, time = None):
        if time is not None:
            time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S").replace(tzinfo=pytz.UTC)
            time = time.astimezone(timezone(settings.TIME_ZONE)).strftime("%Y-%m-%d %H:%M:%S")
        return time