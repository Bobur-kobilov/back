from . import *


# 코인가이드 작성
class CoinGuideCreate(CreateAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "coinguide-create"

    #--------------------------------------
    #  AUTHORITY
    #--------------------------------------
    permission_classes = [CoinGuideCreatePermission]

    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = CoinGuideCreateSerializer
        return serializer
    
    # 쿼리셋 가져오기
    def get_queryset(self):
        return CoinGuide.objects.all()

    def create(self, request, *args, **kwargs):

        parser_classes = (MultiPartParser, FormParser)
        data = {}

        for str in request.data :
            data[str] = request.data[str]

        # session에서 user_id 가져오기
        data['user_id'] = request.user.get_id()

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        # 생선된 pk값 리턴
        instance = serializer.save()
        result = {}
        result['id'] = instance.id
        result['user_id'] = instance.user_id

        headers = self.get_success_headers(serializer.data)

        return Response(data = result, status=status.HTTP_201_CREATED, headers=headers)