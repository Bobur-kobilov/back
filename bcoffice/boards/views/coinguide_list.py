from . import *


# 코인가이드 목록
class CoinGuideList(RawQueryListAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "coinguide-list"

    #--------------------------------------
    #  AUTHORITY
    #--------------------------------------
    # permission_classes = [CoinGuideListPermission]

    #--------------------------------------
    #  PROPERTIES : FILTER
    #--------------------------------------
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
        serializer = CoinGuideSerializer
        return serializer

    # 쿼리셋 가져오기
    def add_filter(self, query = None, status = None, lang = None, currency = None):

        # 작성상태 검색
        if status is not None and status is not '':
            query = RawQuerySyntax.add_where( query, "status = '{0}'".format(status))

        # 작성 언어 검색
        if lang is not None and lang is not '':
            query = RawQuerySyntax.add_where( query, "lang = '{0}'".format(lang))

        if currency is not None and currency is not '':
            query = RawQuerySyntax.add_where( query, "currency = '{0}'".format(currency))

        query = query + ' GROUP BY bc.id'
        return query

    def list(self, request, *args, **kwargs):
        query = """
            SELECT 
                bc.id,
                user_id,
                status,
                title,
                contents,
                name_ko,
                name_en,
                abbr,
                developer,
                algorithm,
                release_date,
                block_time,
                rewards,
                total_volume,
                feature,
                bc.created_at,
                bc.updated_at
            FROM
                boards_coinguide AS bc
            LEFT JOIN
                boards_coinguide_language AS bcl ON bc.id = bcl.board_id
        """

        # 작성상태 검색
        state = request.query_params.get('status')
        
        # 언어 검색
        lang = request.query_params.get('lang')

        currency = request.query_params.get('currency')

        query = self.add_filter (
            query       = query
            , status    = state
            , lang      = lang
            , currency = currency
        )

        if query is None:
            return Response (
                # "일치하는 값이 없습니다."
                data    = ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00008)
                , status = status.HTTP_404_NOT_FOUND
            )

        queryset = self.get_queryset(model=CoinGuide, query=query)#self.filter_queryset(self.get_queryset())

        # 정렬하기
        ordering = request.GET.get('ordering'    , None)

        queryset = self.add_ordering (
            queryset = queryset
            , ordering = ordering
        )
        
        # Pagination 클래스의 인스턴스를 생성한다
        pagination = self.pagination_class()

        # 쿼리셋을 시리얼라이징 한다.
        serializer = self.get_serializer_class()( queryset, many=True)
        
        # pagination.paginate_queryset 메서드를 통해 쿼리셋을 만든다.
        queryset = pagination.paginate_queryset(queryset, request)

        # pagination.get_paginated_response 메서드를 통해 Response객체를 만들어 응답한다.
        return pagination.get_paginated_response( serializer.data )