from . import  *


# STOP 주문내역
class OrderStopList(ListAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "order-stop-list"
    permission_classes = [OrderStopPermission]
    pagination_class = StandardPagination
    #--------------------------------------
    #  PROPERTIES : FILTER
    #--------------------------------------
    filter_fields   = []
    search_fields   = []
    ordering_fields = ['created_at']
    ordering        = ['-created_at']
    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = StopOrderSerializer
        return serializer

    # 쿼리셋 가져오기
    def get_queryset(self, order_id = None, start = None, end = None, member_id = None, trade_class = None, state = None, market = None):
        types = ['id', 'email', 'phone']

        query = StopOrders.objects.using('exchange')

        # 주문번호 검색
        if order_id is not None and order_id is not '':
            query = query.filter(order_id = order_id)

        # 회원검색
        if member_id is not None:
            query = query.filter(member_id = int(member_id))

        # 조회시간 설정
        if start is not None and start is not '' and str(start) != 'Invalid date':
            start_date = start + ' 00:00:00'
            query = query.filter(created_at__gte = start_date)
        if end is not None and end is not '' and str(end) != 'Invalid date':
            end_date = end + ' 23:59:59'
            query = query.filter(created_at__lte = end_date)

        # 매매구분 값
        trade_class_list = ['Bid', 'Ask']            # 전체, 매수, 매도

        # 매매구분 조합
        order_trade_class = ''
        if trade_class is not None and trade_class is not '':
            if trade_class == 'all':
                order_trade_class = order_trade_class
            elif trade_class in trade_class_list:
                order_trade_class = order_trade_class + trade_class
            else:
                return None

        # 매매구분 설정
        if order_trade_class is not '':
            query = query.filter(type__contains = order_trade_class)

        # 상태설정
        if state is not None and state is not '':
            query = query.filter(state = state)

        # 마켓 설정
        if market is not None and market is not '' and market != 'all':
            market = market.split(',')
            # 값이 id값이 아닌 'BTC/EHT' 등 문자값으로 들어오기 때문에 값 변경
            for i in range(len(market)):
                market[i] = selectMarketDic[market[i]]['code']
            query = query.filter(currency__in = market)

        return query


    # email 추가
    def list(self, request, *args, **kwargs):

        # 주문번호 조회
        order_id        = request.GET.get('order_id'    , None)

        # 조회기간선택
        start_date      = request.GET.get('start_date'  , None)
        end_date        = request.GET.get('end_date'    , None)

        # 회원정보로 검색
        member_id       = request.query_params.get('member_id', None)

        # 매매구분 검색
        trade_class     = request.GET.get('trade_class' , None)

        # 상태 검색
        state           = request.GET.get('state'       , None)

        # 마켓 검색
        market          = request.GET.get('market'      , None)

        # 엑셀 여부
        is_excel = bool(request.query_params.get('excel', False))

        queryset = self.get_queryset(
            order_id        = order_id
            , start         = start_date
            , end           = end_date
            , member_id     = member_id
            , trade_class   = trade_class
            , state         = state
            , market        = market
        )

        if queryset is None:
            return Response (
                # "일치하는 값이 없습니다."
                data    = ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00008)
                , status = status.HTTP_404_NOT_FOUND
            )

        queryset = self.filter_queryset(queryset)
        if not is_excel:
            queryset = self.paginate_queryset(queryset)

        serializer = self.get_serializer(queryset, many=True)
        if not is_excel:
            return self.get_paginated_response(serializer.data)
        else:
            return Response({'results': serializer.data})