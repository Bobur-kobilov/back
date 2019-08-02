from . import *


# 추천인정보 지급내역
class MemberReferralPayList(RawQueryListAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "member-referral-payments-list"
    permission_classes = [MemberReferralPayPermission]
    #--------------------------------------
    #  PROPERTIES : FILTER
    #--------------------------------------
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
        serializer = ReferralPaySerializer
        return serializer

    def add_filter(self, query = None, member_id = None, friend_id = None, start_date = None, end_date = None, currency = None):
        query = RawQuerySyntax.add_where(query, "r.member_id = {0}".format(int(member_id)))

        # 검색어 조회
        if friend_id is not None :
            query = RawQuerySyntax.add_where(query, "m.id = {0}".format(int(friend_id)))

        if currency is not None :
            query = RawQuerySyntax.add_where(query, "currency = {0}".format(currency))

        # 날짜 검색
        if start_date is not None and start_date is not '' and str(start_date) != 'Invalid date':
            start_date = set_time_zone(start_date, timezone('UTC'), 'start')
            query = RawQuerySyntax.add_where(query, "rfh.created_at >= '{0}'".format(start_date))
        if end_date is not None and end_date is not '' and str(end_date) != 'Invalid date':
            end_date = set_time_zone(end_date, timezone('UTC'), 'end')
            query = RawQuerySyntax.add_where(query, "rfh.created_at <= '{0}'".format(end_date))

        return query
    
    def list(self, request, *args, **kwargs):
        query = """
            SELECT
                rfh.id              as id
                , trade_id
                , currency
                , amount
                , rfh.fee           as fee
                , rfh.member_id     as member_id
                , rfh.created_at    as created_at
            FROM
                referral_fee_histories as rfh
            INNER JOIN
                referrals as r ON r.referral_id = rfh.referral_id
            INNER JOIN
	            members as m on m.id = rfh.member_id
        """
        member_id = request.query_params.get("member_id", None)
        currency = request.query_params.get("currency", None)
        if member_id is None:
            return Response(
                ResponseMessage.getMessageData(
                    data = ResponseMessage.MESSAGE_ERR00017.format("member_id")
                    , status=status.HTTP_400_BAD_REQUEST)
            )

        # 조회기간선택
        start_date      = request.GET.get('start_date'  , None)
        end_date        = request.GET.get('end_date'    , None)

        friend_id       = request.query_params.get('friend_id', None)
        
        query = self.add_filter(
            query           = query
            , member_id     = member_id
            , friend_id     = friend_id
            , start_date    = start_date
            , end_date      = end_date
            , currency      = currency
        )
        
        if query is None:
            return Response (
                # "일치하는 값이 없습니다."
                data    = ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00008)
                , status = status.HTTP_404_NOT_FOUND
            )

        queryset = self.get_queryset(model=ReferralFriends, query=query, __db__='exchange')

        # Pagination 클래스의 인스턴스를 생성한다
        pagination = self.pagination_class()
        
        # 쿼리셋을 시리얼라이징 한다.
        serializer = self.get_serializer_class()( queryset, many=True)
        
        # pagination.paginate_queryset 메서드를 통해 쿼리셋을 만든다.
        queryset = pagination.paginate_queryset(queryset, request, __db__ = 'exchange')

        # pagination.get_paginated_response 메서드를 통해 Response객체를 만들어 응답한다.
        return pagination.get_paginated_response( serializer.data )