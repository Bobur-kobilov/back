from . import *


# Daily뉴스 첨부파일 생성
class DailyNewsAttachCreate(CreateAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "daily-attach-create"

    #--------------------------------------
    #  AUTHORITY
    #--------------------------------------
    permission_classes = [DailyNewsAttachCreatePermission]

    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 첨부파일작성 시리얼라이저
    def get_serializer_class(self):
        serializer = FileAttachmentCreateSerializer
        return serializer

    # 맵핑테이블작성 시리얼라이저
    def get_serializer_mapping(self, *args, **kwargs):
        serializer_class = DailyNewsMappingCreateSerializer
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)
    
    # 쿼리셋 가져오기
    def get_queryset(self):
        return FileAttachment.objects.all()

    def create(self, request, *args, **kwargs):

        parser_classes = (MultiPartParser, FormParser)
        data = {}

        for str in request.data :
            data[str] = request.data[str]
        
        # type이 normal이나 primary이어야 함 (normal : 일반 / primary : 표지)
        attach_type = ['normal', 'primary']

        if not data['type'] in attach_type:
            return Response(
                    # "type을 'normal', 'primary'로 설정해 주세요."
                    data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00006)
                    , status=status.HTTP_400_BAD_REQUEST
                )

        return_data = {}
        # 첨부파일
        if data['type'] == 'normal':
            # 파일테이블에 저장
            file = request.FILES['files']
            data['file_name'] = file.name
            
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()

            # id값 추가하여 리턴
            for str in serializer.data:
                return_data[str]  = serializer.data[str]
            return_data['id'] = instance.id

            # 맵핑테이블에 저장
            mapping_data = {}
            mapping_data['board_id']     = request.data['target']
            mapping_data['file_info_id'] = instance.id
            
            serializer = self.get_serializer_mapping(data=mapping_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        # 표지이미지
        elif data['type'] == 'primary':
            # 기존표이지이미가 있으면 제거
            daily_primary = DailyNews.objects.filter(id = data['target'])
            daily_primary_id = None
            for obj in daily_primary:
                daily_primary_id = obj.primary_image_id
            file_primary = FileAttachment.objects.filter(id = daily_primary_id)
            if file_primary.exists():
                file_primary.delete()

            # 파일테이블에 저장
            file = request.FILES['files']
            data['file_name'] = file.name
            
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()

            # id값 추가하여 리턴
            for str in serializer.data:
                return_data[str]  = serializer.data[str]
            return_data['id'] = instance.id

            # 파일테이블ID 반영
            daily = {}
            for obj in daily_primary:
                daily = obj
            daily.primary_image_id = instance.id
            daily.save()

        headers = self.get_success_headers(serializer.data)
        return Response(data = return_data, status=status.HTTP_201_CREATED, headers=headers)