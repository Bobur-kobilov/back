from . import *

# 사용자 패스워드 변경(관리자용)
class UserPasswordUpdate(UpdateAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "user-password-update"
    permission_classes = [UserUpdatePermission]
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

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    # 응답처리
    def put(self, request, *args, **kwargs):
        instance = User.objects.get(pk=kwargs.get("pk"))
        data = {}
        data["new_password"] = request.data.get("new_password")
        data["old_password"] = instance.password

        serializer = self.get_serializer_class()(data = data)

        if serializer.is_valid():
            instance.set_password(serializer.data.get("new_password"))
            instance.save()

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)