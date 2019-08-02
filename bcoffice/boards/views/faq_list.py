from . import *

# FAQ 목록
class FaqList(RawQueryListAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "faq-list"

    #--------------------------------------
    #  AUTHORITY
    #--------------------------------------
    # permission_classes  = [FaqListPermission]
    
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
        serializer = FaqSerializer
        return serializer
    
    # 쿼리셋 가져오기
    def add_filter(self, query = None, start = None, end = None, faq_category = None, emp_no = None, search = None, lang = None):
        
        # 작성일시 설정 (UTC 시간으로 변경 후 쿼리 실행)
        if start is not None and start is not '' and str(start) != 'Invalid date':
            start_date = set_time_zone(start, timezone('UTC'), 'start')
            query = RawQuerySyntax.add_where( query, "bf.created_at >= '{0}'".format(start_date))
        if end is not None and end is not '' and str(end) != 'Invalid date':
            end_date = set_time_zone(end, timezone('UTC'), 'end')
            query = RawQuerySyntax.add_where( query, "bf.created_at <= '{0}'".format(end_date))

        # 전체보기(1) 제외
        if faq_category is not None and faq_category is not '' and int(faq_category) != 1:
            query = RawQuerySyntax.add_where( query, "faq_category_id = {0}".format(faq_category))

        # 작성자 ID 검색
        if emp_no is not None and emp_no is not '':
            query = RawQuerySyntax.add_where( query, "au.emp_no = {0}".format(emp_no))
        
        # 제목, 내용 검색
        if search is not None and search is not '':
            query = RawQuerySyntax.add_where(
                query
                , "(title LIKE CONCAT('%%','{0}','%%') or contents LIKE CONCAT('%%','{0}','%%'))".format(search)
            )

        # 작성 언어 검색
        if lang is not None and lang is not '':
            query = RawQuerySyntax.add_where( query, "bfl.lang = '{0}'".format(lang))

        query = query + ' GROUP BY bf.id'
        return query

    def list(self, request, *args, **kwargs):
        # 언어 검색
        lang            = request.query_params.get('lang', None)

        query = """
            SELECT 
                bf.id
                , title
                , contents
                , read_count
                , bf.created_at
                , bf.updated_at
                , faq_category_id
                , user_id
            FROM
                boards_faq as bf
            INNER JOIN
                boards_faq_category as bfc
            ON
                bf.faq_category_id = bfc.category_id
            INNER JOIN
                account_user as au
            ON
                bf.user_id = au.id
            LEFT JOIN
                boards_faq_language as bfl
            ON
                bf.id = bfl.board_id
        """

        # 작성일시 선택
        start_date      = request.query_params.get('start_date', None)
        end_date        = request.query_params.get('end_date', None)

        # 카테고리 선택
        faq_category    = request.query_params.get('faq_category', None)

        # 작성자 검색
        emp_no         = request.query_params.get('emp_no', None)

        # 제목, 내용 검색
        search          = request.query_params.get('search', None)

        query    = self.add_filter(
            query           = query
            , start         = start_date
            , end           = end_date
            , faq_category  = faq_category
            , emp_no        = emp_no
            , search        = search
            , lang          = lang
        )

        if query is None:
            return Response (
                # "일치하는 값이 없습니다."
                data    = ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00008)
                , status = status.HTTP_404_NOT_FOUND
            )

        queryset = self.get_queryset(model=Faq, query=query)
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
        
        # pagination.paginate_queryset 메서드를 통해 쿼리셋을 만든다.
        queryset = pagination.paginate_queryset(queryset, request, count = len(list(Faq.objects.raw(query))))

        category_dict = {}
        if lang is not None:
            pass
        else:
            lang = 'ko'
        language = FaqCategory.objects.values('category', 'category_id').filter(lang=lang)
        for item in language:
            category_dict[item['category_id']] = item['category']
        for item in serializer.data:
            item['faq_category'] = category_dict[item['faq_category_id']]

        # pagination.get_paginated_response 메서드를 통해 Response객체를 만들어 응답한다.
        return pagination.get_paginated_response( serializer.data )
