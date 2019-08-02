from . import *

# 권한 목록 가져오기
class DeptCreateList(ListCreateAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "dept-list"
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

    # 응답하기
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)