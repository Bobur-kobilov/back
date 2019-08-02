from . import *


# 코인가이드 로고 생성
class CoinGuideAttachCreate(CreateAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "coinguide-attach-create"

    #--------------------------------------
    #  AUTHORITY
    #--------------------------------------
    permission_classes = [CoinGuideAttachCreatePermission]

    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = FileAttachmentCreateSerializer
        return serializer
    
    # 쿼리셋 가져오기
    def get_queryset(self):
        return FileAttachment.objects.all()

    def create(self, request, *args, **kwargs):

        parser_classes = (MultiPartParser, FormParser)
        data = {}

        for str in request.data :
            data[str] = request.data[str]

        item = CoinGuide.objects.get(pk = data['target'])

        # 기존 파일의 유무 파악 후 있으면 삭제
        if data['type'] == 'logo':
            file_item = FileAttachment.objects.filter(id = item.logo_id)
        elif data['type'] == 'icon':
            file_item = FileAttachment.objects.filter(id = item.icon_id)

        if file_item.exists():
            file_item.delete()
        
        # 파일테이블에 저장
        file = request.FILES['files']
        data['file_name'] = file.name
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        # id값 추가하여 리턴
        return_data = {}
        for str in serializer.data:
            return_data[str]  = serializer.data[str]
        return_data['id'] = instance.id

        # 파일테이블ID 반영
        coinguide = {}
        coinguide = item

        if data['type'] == 'logo':
            coinguide.logo_id = instance.id
        elif data['type'] == 'icon':
            coinguide.icon_id = instance.id
        
        coinguide.save()

        headers = self.get_success_headers(serializer.data)
        return Response(data = return_data, status=status.HTTP_201_CREATED, headers=headers)