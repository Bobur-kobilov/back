from . import *


class DeptDutyDetail(RetrieveUpdateDestroyAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "dept-Duty-detail"
    permission_classes = [DeptDutyPermission]
    #--------------------------------------
    #  PROPERTIES : FILTER
    #--------------------------------------
    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = DepartmentDutySerializer
        return serializer

    # 쿼리셋 가져오기
    def get_queryset(self):
        return DepartmentDuty.objects.all()

    # 삭제기능 제거
    def delete(self, request, *args, **kwargs):
        return Response(data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00016) ,status=status.HTTP_406_NOT_ACCEPTABLE)