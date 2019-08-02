from . import *


# 코인가이드 유용한링크 생성
class CoinGuideUsefulLinkCreate(CreateAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "coinguide-link-create"

    #--------------------------------------
    #  AUTHORITY
    #--------------------------------------
    permission_classes = [CoinGuideUsefulLinkCreatePermission]

    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = CoinGuideUsefulLinkCreateSerializer
        return serializer
    
    # 쿼리셋 가져오기
    def get_queryset(self):
        return CoinGuideUsefulLink.objects.all()

    def create(self, request, *args, **kwargs):

        parser_classes = (MultiPartParser, FormParser)
        data = {}

        for str in request.data :
            data[str] = request.data[str]

        # 해당게시물 번호
        data['post_id'] = request.data['target']

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        # id값 추가하여 리턴
        return_data = {}
        for str in serializer.data:
            return_data[str]  = serializer.data[str]
        return_data['id'] = instance.id

        headers = self.get_success_headers(serializer.data)
        return Response(data = return_data, status=status.HTTP_201_CREATED, headers=headers)