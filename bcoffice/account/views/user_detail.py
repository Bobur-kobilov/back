from . import *

# 사용자 상세정보 가져오기
class UserDetail(RetrieveAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "user-detail"

    #--------------------------------------
    #  PROPERTIES : FILTER
    #--------------------------------------
    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = UserSerializer
        return serializer

    # 쿼리셋 가져오기
    def get_queryset(self):
        return User.objects.all()