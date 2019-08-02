from . import *


# 공지사항 목록
class NoticeList(RawQueryListAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "notice-list"

    #--------------------------------------
    #  AUTHORITY
    #--------------------------------------
    #permission_classes = [NoticeListPermission]

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
        serializer = NoticeSerializer
        return serializer
 
    # 쿼리셋 가져오기
    def add_filter(self, query = None, start = None, end = None, emp_no = None, status = None, search = None, lang = None):
        
        # 작성일시 설정
        if start is not None and start is not '' and str(start) != 'Invalid date':
            start_date = set_time_zone(start, timezone('UTC'), 'start')
            query = RawQuerySyntax.add_where( query, "bn.created_at >= '{0}'".format(start_date))
        if end is not None and end is not '' and str(end) != 'Invalid date':
            end_date = set_time_zone(end, timezone('UTC'), 'end')
            query = RawQuerySyntax.add_where( query, "bn.created_at <= '{0}'".format(end_date))

        # 작성자 ID 검색
        if emp_no is not None and emp_no is not '':
            query = RawQuerySyntax.add_where( query, "au.emp_no = {0}".format(emp_no))
        
        # 작성상태 검색
        if status is not None and status is not '':
            query = RawQuerySyntax.add_where( query, "bn.status = '{0}'".format(status))

        # 제목, 내용 검색
        if search is not None and search is not '':
            query = RawQuerySyntax.add_where(
                query
                , "(title LIKE CONCAT('%%','{0}','%%') or contents LIKE CONCAT('%%','{0}','%%'))".format(search)
            )

        # 작성 언어 검색
        if lang is not None and lang is not '':
            query = RawQuerySyntax.add_where( query, "lang = '{0}'".format(lang))

        query = query + ' GROUP BY bn.id'
        return query

    def list(self, request, *args, **kwargs):
        query = """
            SELECT 
                bn.id
                , notice
                , bn.status
                , title
                , contents
                , read_count
                , bn.created_at
                , bn.updated_at
                , user_id
                , emp_no
                , send_email
                , send_sms
            FROM
                boards_notice as bn
            INNER JOIN
                account_user as au ON au.id = bn.user_id
            LEFT JOIN
                boards_notice_language as bnl ON bn.id = bnl.board_id
        """

        # 작성일시 선택
        start_date      = request.GET.get('start_date')
        end_date        = request.GET.get('end_date')

        # 작성자 검색
        emp_no         = request.query_params.get('emp_no')

        # 작성상태 검색
        state           = request.query_params.get('status')

        # 제목, 내용 검색
        search          = request.query_params.get('search')

        # 언어 검색
        lang            = request.query_params.get('lang')

        query = self.add_filter(
            query           = query
            , start         = start_date
            , end           = end_date
            , emp_no        = emp_no
            , status        = state
            , search        = search
            , lang          = lang
        )

        if query is None:
            return Response (
                # "일치하는 값이 없습니다."
                data    = ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00008)
                , status = status.HTTP_404_NOT_FOUND
            )

        queryset = self.get_queryset(model=Notice, query=query)#self.filter_queryset(self.get_queryset())

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