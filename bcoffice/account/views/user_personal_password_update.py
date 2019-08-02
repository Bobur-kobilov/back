from . import *

# 사용자 패스워드 변경(개인용)
class UserPersonalPasswordUpdate(UpdateAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "user-personal-password-update"
    permission_classes = [permissions.IsAuthenticated]
    #--------------------------------------
    #  PROPERTIES : FILTER
    #--------------------------------------
    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = UserPasswordUpdateSerializer
        return serializer

    # 쿼리셋 가져오기
    def get_queryset(self):
        return User.objects.all()

    # 응답처리
    def put(self, request, *args, **kwargs):
        user_id = request.user.get_id()
        self.object = User.objects.get(pk=user_id)
        serializer = self.get_serializer_class()(data = request.data)

        if serializer.is_valid():
            old_password = serializer.data.get("old_password")

            if not self.object.check_password(old_password):
                return Response(
                    data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00028)
                    , status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)