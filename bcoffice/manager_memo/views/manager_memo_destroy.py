from . import *


# 관리자 메시지 삭제
class ManagerMemoDestory(DestroyAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "manager-memo-destroy"
    permission_classes = [ManagerMemoDestroyPermission]
    #--------------------------------------
    #  PROPERTIES : FILTER
    #--------------------------------------
    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이즈 클래스 가져오기
    def get_serializer_class(self):
        serializer = ManagerMemoSerializer
        return serializer

    # 쿼리셋 가져오기
    def get_queryset(self):
        return ManagerMemo.objects.all()

    # 삭제하기
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if( instance.user_id == request.user.get_id()):
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
                data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00005)
                , status=status.HTTP_403_FORBIDDEN
            )