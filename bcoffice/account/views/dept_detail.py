from . import *

class DeptDetail(RetrieveUpdateDestroyAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "dept-detail"
    permission_classes = [DeptTypePermission]
    #--------------------------------------
    #  PROPERTIES : FILTER
    #--------------------------------------
    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = DepartmentTypeSerializer
        return serializer

    # 쿼리셋 가져오기
    def get_queryset(self):
        return DepartmentType.objects.all()

    # 삭제기능 제거
    def delete(self, request, *args, **kwargs):
        return Response(data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00016), status=status.HTTP_406_NOT_ACCEPTABLE)