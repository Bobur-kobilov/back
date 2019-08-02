from . import *


# 1:1 문의내역 처리상태별 갯수 표시하기 위한 pagination set
class CustomPagination(RawQuerySetPagination):
    def get_paginated_response(self, data, count):
        return Response({
            'info' : QuestionList.countAmount(self)
            , 'count' : len(list(Question.objects.raw(count)))
            , 'results' : data
        })

def question_query():
    query = """
        SELECT
            q.id					AS id
            , q.member_id			AS member_id
            , q.status				AS status
            , q.title				AS title
            , q.contents			AS contents
            , q.created_at			AS created_at
            , q.updated_at			AS updated_at
            , q.question_type_id	AS question_type_id
            , u.id					AS user_id
            , u.emp_no				AS emp_no
        FROM
            support_questions as q
        LEFT JOIN
            support_answers as a
        ON
            q.id = a.target_id
        LEFT JOIN
            account_user as u
        ON
            a.user_id = u.id
    """
    return query

# 1:1 문의 내역 조회
class QuestionList(RawQueryListAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "question-list"

    #--------------------------------------
    #  AUTHORITY
    #--------------------------------------
    # permission_classes = [QuestionPermission]

    #--------------------------------------
    #  PROPERTIES : FILTER
    #--------------------------------------
    filter_fields   = []
    search_fields   = []
    ordering_fields = []
    ordering        = []
    pagination_class    = CustomPagination
    page_size_query_param = ""

    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = QuestionSerializer
        return serializer

    def add_filter(self, query = None, start = None, end = None, member_id = None, status = None, question_type = None, emp_no = None):
        # 회원정보로 검색
        if member_id is not None:
            query = RawQuerySyntax.add_where(query, "q.member_id = {0}".format(int(member_id)))

        # 조회시간 설정
        if start is not None and start is not '' and str(start) != 'Invalid date':
            start_date = set_time_zone(start, timezone('UTC'), 'start')
            query = RawQuerySyntax.add_where(query, "q.created_at >= '{0}'".format(start_date))
        if end is not None and end is not '' and str(end) != 'Invalid date':
            end_date = set_time_zone(end, timezone('UTC'), 'end')
            query = RawQuerySyntax.add_where(query, "q.created_at <= '{0}'".format(end_date))

        # 작성상태 검색
        if status is not None and status is not '':
            query = RawQuerySyntax.add_where(query, "q.status = '{0}'".format(status))

        # 질문분류 검색
        if question_type is not None and question_type is not '':
            query = RawQuerySyntax.add_where(query, "q.question_type_id = {0}".format(question_type))

        # 답변자 검색
        if emp_no is not None and emp_no is not '':
            query = RawQuerySyntax.add_where(query, "u.emp_no = '{0}'".format(emp_no))

        return query


    # email 추가
    def list(self, request, *args, **kwargs):
        query = question_query()

        # 조회기간선택
        start_date      = request.GET.get('start_date'  , None)
        end_date        = request.GET.get('end_date'    , None)

        # 작성자 검색
        member_id       = request.query_params.get('member_id', None)

        # 작성상태 검색
        status_type      = request.GET.get('status', None)

        # 질문유형 검색
        question_type   = request.GET.get('question_type', None)

        # 답변자 검색
        emp_no   = request.GET.get('emp_no', None)

        # 언어 검색
        lang = request.query_params.get('lang', None)

        query = self.add_filter(
            query           = query
            , start         = start_date
            , end           = end_date
            , member_id     = member_id
            , status        = status_type
            , question_type = question_type
            , emp_no        = emp_no
        )

        if query is None:
            return Response (
                # "일치하는 값이 없습니다."
                data    = ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00022)
                , status = status.HTTP_404_NOT_FOUND
            )

        queryset = self.get_queryset(model=Question, query=query)#self.filter_queryset(self.get_queryset())

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
        queryset = pagination.paginate_queryset(queryset, request)

        category_dict = {}
        if lang is not None:
            language = QuestionType.objects.values('type', 'category_id').filter(lang=lang)
            for item in language:
                category_dict[item['category_id']] = item['type']
        for item in serializer.data:
            if lang is not None:
                item['question_type'] = category_dict[item['question_type_id']]

        # 거래소 이용자 정보 추가
        for item in serializer.data:
            member = Members.objects.using('exchange').values('display_name','email', 'phone_number').filter(id=item['member_id'])
            for obj in member:
                item['member_name']  = obj['display_name']
                item['member_email'] = obj['email']
                item['member_phone'] = obj['phone_number']

        return pagination.get_paginated_response( serializer.data , count = query )

    # 상단 정보 중 전체, 완료(CPLT), 처리중(PROC), 대기(WAIT) 갯수
    def countAmount(self):
        count_queryset = Question.objects.values('status').annotate(count_status=Count('status'))
        count_value = {}

        supportInfoDic = {
            'ALL'   : {"code": "all"},
            'WAIT'  : {"code": "wait"},
            'PROC'  : {"code": "ing"},
            'CPLT'  : {"code": "done"}
        }

        # 상단 정보 초기화 (해당 인덱스가 없을 수도 있기 때문에)
        count_value[supportInfoDic['ALL']['code']] = 0
        count_value[supportInfoDic['WAIT']['code']] = 0
        count_value[supportInfoDic['PROC']['code']] = 0
        count_value[supportInfoDic['CPLT']['code']] = 0

        for obj in count_queryset:
            count_value['all'] += obj['count_status']      # all에 값 누적
            count_value[supportInfoDic[obj['status']]['code']] = obj['count_status']

        return count_value