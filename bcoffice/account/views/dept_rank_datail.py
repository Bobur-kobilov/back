from . import *


class DeptRankDetail(RetrieveUpdateDestroyAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "dept-rank-detail"
    permission_classes = [DeptRankPermission]
    #--------------------------------------
    #  PROPERTIES : FILTER
    #--------------------------------------
    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = DepartmentRankSerializer
        return serializer

    # 쿼리셋 가져오기
    def get_queryset(self):
        return DepartmentRank.objects.all()

    # 삭제기능 제거
    def delete(self, request, *args, **kwargs):
        return Response(data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00016), status=status.HTTP_406_NOT_ACCEPTABLE)