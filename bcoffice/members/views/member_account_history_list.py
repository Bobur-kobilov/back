from . import *


# 회원 자산변동 이력
class MemberAccountHistoryList(ListAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "member-account-list"
    permission_classes = [MemberAccountHistoryPermission]
    #--------------------------------------
    #  PROPERTIES : FILTER
    #--------------------------------------
    ordering_fields     = ['id']
    ordering            = ['-id']
    pagination_class    = StandardPagination
    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = MemberAccountHistorySerializer
        return serializer
    
    # 쿼리셋 가져오기
    def get_queryset(self, member_id = None, start = None, end = None, currency = None):
        query = AccountVersions.objects.using("exchange").filter(member_id = member_id)
        
        # 조회기간 설정
        if start is not None and start is not '' and str(start) != 'Invalid date':
            start_date = start + ' 00:00:00'
            query = query.filter(created_at__gte = start_date)
        if end is not None and end is not '' and str(end) != 'Invalid date':
            end_date = end + ' 23:59:59'
            query = query.filter(created_at__lte = end_date)

        # 코인 설정
        if currency is not None:
            query = query.filter(currency = currency)

        return query

    def list(self, request, *args, **kwargs):
        member_id = request.query_params.get("member_id", None)

        if member_id is None:
            return Response (
                # "회원검색 값을 넣어주세요."
                data    = ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00007)
                ,status = status.HTTP_400_BAD_REQUEST
            )

        # 조회기간선택
        start_date      = request.query_params.get('start_date'  , None)
        end_date        = request.query_params.get('end_date'    , None)

        # 코인선택
        currency        = request.query_params.get('currency', None)

        # 엑셀 여부
        is_excel = bool(request.query_params.get('excel', False))

        queryset = self.get_queryset(
            member_id       = member_id
            , start         = start_date
            , end           = end_date
            , currency      = currency
        )

        if queryset is None:
            return Response (
                # "일치하는 값이 없습니다."
                data    = ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00008)
                ,status = status.HTTP_404_NOT_FOUND
            )
            
        queryset = self.filter_queryset(queryset)
        if not is_excel:
            queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        if not is_excel:
            return self.get_paginated_response(serializer.data)
        else:
            return Response({'results': serializer.data})