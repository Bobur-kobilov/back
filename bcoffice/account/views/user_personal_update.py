from . import *

# 사용자 일반 정보 업데이트(패스워드 업데이트는 UserPasswordUpdate를 통해 실행)
# 사용자 본인의 정보 업데이트
class UserPersonalUpdate(UpdateAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "user-personal-update"
    permission_classes = [permissions.IsAuthenticated]
    #--------------------------------------
    #  PROPERTIES : FILTER
    #--------------------------------------
    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = UserPersonalUpdateSerializer
        return serializer

    # 쿼리셋 가져오기
    def get_queryset(self):
        return User.objects.all()

    def put(self, request, *args, **kwargs):
        """
        혹여 사용자 ID 값이 넘어왔을 때
        세션 사용자 정보의 ID 값과 비교해 다를 경우 403 에러로 응답한다.
        """
        user_id = request.data.get("id", None)
        if request.data.get("id", None) :
            user_id = int(user_id)
            if request.user.get_id() is not user_id :
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            user_id = request.user.get_id()

        instance = User.objects.get(pk=user_id)

        """
        사용자 정보수정은 name과 cell_phone만 수정하기 때문에 partial은 항상 True가 된다.
        """
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


    def patch(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)