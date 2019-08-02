from . import *

class UserCreate(CreateAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "user-create"
    permission_classes = [UserCreatePermission]
    #--------------------------------------
    #  PROPERTIES : FILTER
    #--------------------------------------
    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = UserCreateSerializer
        return serializer

    # 쿼리셋 가져오기
    def get_queryset(self):
        return User.objects.all()

    def create(self, request, *args, **kwargs):
        data = {}

        for field in request.data:
            data[field] = request.data.get(field)

        if not request.data.get("eng_name", False):
            data['eng_name'] = None

        if not request.data.get("active", False):
            data['active'] = True

        if not request.data.get("status", False):
            data['status'] = STATUS['ACTV']

        if not request.data.get("close_date, False"):
            data['close_date'] = None

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)