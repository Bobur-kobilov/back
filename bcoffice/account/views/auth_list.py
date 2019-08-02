from . import *

# 권한 목록 가져오기
class AuthList(ListAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "auth-list"
    permission_classes = [AuthListCreatePermission]
    #--------------------------------------
    #  PROPERTIES : FILTER
    #--------------------------------------
    filter_fields = ['user_id']
    pagination_class = LimitOffsetPagination
    page_size_query_param = ""
    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = AuthSerializer
        return serializer

    # 쿼리셋 가져오기
    def get_queryset(self):
        return Auth.objects.all()

    # 응답하기
    def list(self, request):
        if request.query_params.get("user_id", False):
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        return Response(data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00015), status=status.HTTP_400_BAD_REQUEST)