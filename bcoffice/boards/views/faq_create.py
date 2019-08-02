from . import *

# FAQ 작성
class FaqCreate(CreateAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "faq-create"

    #--------------------------------------
    #  AUTHORITY
    #--------------------------------------
    permission_classes = [FaqCreatePermission]

    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = FaqCreateSerializer
        return serializer
    
    # 쿼리셋 가져오기
    def get_queryset(self):
        return Faq.objects.all()
    
    # 작성언어 시리얼라이징
    def get_lang_serializer(self, *args, **kwargs):
        serializer_class = FaqLanguageCreatedSerializer
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    # FAQ 작성
    def create(self, request, *args, **kwargs):
        data = {}

        for str in request.data :
            data[str] = request.data[str]

        # session에서 user_id 가져오기
        data['user_id'] = request.user.get_id()

        if data['faq_category_id'] is None or int(data['faq_category_id']) == 1:
            return Response(
                    # "카테고리를 선택해주세요.."
                    data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00014)
                    , status=status.HTTP_400_BAD_REQUEST
                )

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        # 작성언어 추가
        lang_data = {}
        try:
            lang = data['lang'].split(',')
            for count in range(len(lang)):
                lang_data['board_id'] = instance.id
                lang_data['lang'] = lang[count]
                lang_serializer = self.get_lang_serializer(data=lang_data)
                lang_serializer.is_valid(raise_exception=True)
                lang_serializer.save()
        except:
            pass

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)