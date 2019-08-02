from . import *
import uuid

# 공지사항 첨부파일 생성
class NoticeAttachCreate(CreateAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "notice-attach-create"

    #--------------------------------------
    #  AUTHORITY
    #--------------------------------------
    permission_classes = [NoticeAttachCreatePermission]

    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = FileAttachmentCreateSerializer
        return serializer

    # 맵핑테이블작성 시리얼라이저
    def get_serializer_mapping(self, *args, **kwargs):
        serializer_class = NoticeMappingCreateSerializer
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)
    
    # 쿼리셋 가져오기
    def get_queryset(self):
        return FileAttachment.objects.all()

    def create(self, request, *args, **kwargs):
        file_type = request.data['type']

        if file_type == 'link':
            image = request.FILES['files']
            up_file = image
            extention_split = up_file.name.split(".")
            extention = extention_split[extention_split.__len__() - 1]
            file_name = str(uuid.uuid4()) + "." + extention
            dt = datetime.now().strftime('/%Y/%m/%d/')
            key = 'static' + dt + file_name

            s3 = boto3.resource('s3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

            client = s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)

            response = client.put_object(
            Key=key
            , Body=up_file.read()
            , ACL = 'public-read'
            )
            image_link = "https://" + settings.AWS_S3_CUSTOM_DOMAIN + "/" + key
            return Response(data = image_link, status=status.HTTP_201_CREATED)
        else:
            parser_classes = (MultiPartParser, FormParser)
            data = {}

            for str_old in request.data :
                data[str_old] = request.data[str_old]

            # 파일테이블에 저장
            file = request.FILES['files']
            data['file_name'] = file.name

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()

            # id값 추가하여 리턴
            return_data = {}
            for str_old in serializer.data:
                return_data[str_old]  = serializer.data[str_old]
            return_data['id'] = instance.id

            # 맵핑테이블에 저장
            mapping_data = {}
            mapping_data['board_id']     = request.data['target']
            mapping_data['file_info_id'] = instance.id
            
            serializer = self.get_serializer_mapping(data=mapping_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            headers = self.get_success_headers(serializer.data)
            return Response(data = return_data, status=status.HTTP_201_CREATED, headers=headers)