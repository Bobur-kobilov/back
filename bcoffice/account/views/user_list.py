from . import *


# 사용자 목록 가져오기
class UserList(RawQueryListAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "user-list"
    permission_classes = [UserListPermission]
    #--------------------------------------
    #  PROPERTIES : FILTER
    #--------------------------------------
    having_fields = ['role']
    # filter_fields = ['au.id, active']
    # search_fields = ['email']
    ordering_fields = ['au.id', 'email', 'created_at']
    group_fields = ['au.id', 'email']
    ordering = ['-au.id']
    pagination_class = RawQuerySetPagination
    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = UserSerializer
        return serializer

    # 응답하기
    def list(self, request):
        query = """
            SELECT
                au.id
                , password
                , email
                , active
                , created_at
                , updated_at
                , role
            FROM
                account_user as au
            INNER JOIN
                account_auth as aa ON au.id = aa.user_id
        """

        # QuerySet을 먼저 만든다
        queryset = self.get_queryset(model=User, query=query)#self.filter_queryset(self.get_queryset())

        params = request.query_params

        if params.get("search_type", None):
            """이름"""
            if params.get("search_type") == 'name':
                queryset = self.add_filter("name__contain", params.get("search_value"), queryset)
            """email"""
            if params.get("search_type") == 'email':
                queryset = self.add_filter("email__contain", params.get("search_value"), queryset)
            """휴대전화번호"""
            if params.get("search_type") == 'phone':
                queryset = self.add_filter("cell_phone__contain", params.get("search_value"), queryset)

        """사원번호"""
        if params.get("emp_no", None):
            queryset = self.add_filter("emp_no", params.get("emp_no"), queryset)
        """입사일(시작)"""
        if params.get("joined_start", None):
            queryset = self.add_filter("joined_date__gte", params.get("joined_start"), queryset)
        """입사일(끝)"""
        if params.get("joined_end", None):
            queryset = self.add_filter("joined_date__lte", params.get("joined_end"), queryset)
        """해지일(시작)"""
        if params.get("close_start", None):
            queryset = self.add_filter("close_date__gte", params.get("close_start"), queryset)
        """해지일(끝)"""
        if params.get("close_end", None):
            queryset = self.add_filter("close_date__lte", params.get("close_end"), queryset)
        """소속부서"""
        if params.get("dept_type", None):
            queryset = self.add_filter("dept_type_id", params.get("dept_type"), queryset)

        # Pagination 클래스의 인스턴스를 생성한다
        pagination = self.pagination_class()

        # 쿼리셋을 시리얼라이징 한다.
        serializer = self.get_serializer_class()( queryset, many=True)

        # pagination.paginate_queryset 메서드를 통해 쿼리셋을 만든다.
        queryset = pagination.paginate_queryset(queryset, request)

        # pagination.get_paginated_response 메서드를 통해 Response객체를 만들어 응답한다.
        return pagination.get_paginated_response( serializer.data )