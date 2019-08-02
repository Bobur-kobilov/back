from . import *


# 회원 활동내역
class MemberActiveHistoryList(ListAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "member-history-list"
    permission_classes = [MemberActiveHistoryPermission]
    #--------------------------------------
    #  PROPERTIES : FILTER
    #--------------------------------------
    filter_fields       = []
    search_fields       = []
    ordering_fields     = ['created_at']
    ordering            = ['-created_at']
    pagination_class    = StandardPagination
    page_size_query_param = ""
    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = LogInSerializer
        return serializer
    
    # 쿼리셋 가져오기
    def get_queryset(self, start = None, end = None, member_id = None, ip=None):
        types = ['id', 'email', 'phone']
        
        query = SignupHistories.objects.using('exchange')

        # 회원검색
        if member_id is not None:
            query = query.filter(member_id = int(member_id))
        if ip is not None:
            query = query.filter(ip=ip)

        # 조회시간 설정
        if start is not None and start is not '' and str(start) != 'Invalid date':
            start_date = start + ' 00:00:00'
            query = query.filter(created_at__gte = start_date)
        if end is not None and end is not '' and str(end) != 'Invalid date':
            end_date = end + ' 23:59:59'
            query = query.filter(created_at__lte = end_date)
        
        return query

    def list(self, request, *args, **kwargs):
                        
        # 조회기간선택
        start_date      = request.GET.get('start_date'  , None)
        end_date        = request.GET.get('end_date'    , None)

        # 회원정보로 검색
        member_id       = request.query_params.get('member_id', None)
        ip = request.query_params.get('ip', None)

        queryset = self.get_queryset(
            start           = start_date
            , end           = end_date
            , member_id     = member_id
            , ip = ip
        )
    
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)