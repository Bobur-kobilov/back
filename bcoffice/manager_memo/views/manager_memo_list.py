from . import *


# 관리자 메시지 목록 View
class ManagerMemoList(ListAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "manager-memo-list"
    permission_classes = [ManagerMemoListPermission]
    #--------------------------------------
    #  PROPERTIES : FILTER
    #--------------------------------------
    ordering_fields = ['id, created_at']
    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    def get_queryset(self, target_id):
        query = ManagerMemo.objects.all()
        query = query.filter(target_id=target_id)

        return query

    def get_serializer_class(self):
        serializer = ManagerMemoSerializer
        return serializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset(target_id=kwargs['target_id'])
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)