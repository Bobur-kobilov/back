from . import *


# 관리자 메시지 작성
class ManagerMemoCreate(CreateAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "manager-memo-create"
    permission_classes = [ManagerMemoListPermission]
    #--------------------------------------
    #  PROPERTIES : FILTER
    #--------------------------------------
    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이즈 클래스 가져오기
    def get_serializer_class(self):
        serializer = ManagerMemoCreateSerializer
        return serializer

    # 쿼리셋 가져오기
    def get_queryset(self):
        return ManagerMemo.objects.all()

    # 메모 생성하기
    def create(self, request, *args, **kwargs):
        data = {}

        for str in request.data :
            data[str] = request.data[str]

        # session에서 user_id 가져오기
        data['user_id'] = request.user.get_id()

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED, headers=headers)