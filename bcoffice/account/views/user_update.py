from . import *

# 사용자 일반 정보 업데이트(패스워드 업데이트는 UserPasswordUpdate를 통해 실행)
# 관리자 전용 API
class UserUpdate(UpdateAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "user-update"
    permission_classes = [UserUpdatePermission]
    #--------------------------------------
    #  PROPERTIES : FILTER
    #--------------------------------------
    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = UserUpdateSerializer
        return serializer

    # 쿼리셋 가져오기
    def get_queryset(self):
        return User.objects.all()