from . import *


# 1:1 문의 작성
class QuestionCreate(CreateAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "question-create"

    #--------------------------------------
    #  AUTHORITY
    #--------------------------------------
    # POST 메서드 사용이며, 내부사용으로 인해서 권한 제한 제거

    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = QuestionCreateSerializer
        return serializer

    # 쿼리셋 가져오기
    def get_queryset(self):
        return Question.objects.all()

    # 1:1 문의 작성
    def create(self, request, *args, **kwargs):
        data = {}

        for str in request.POST :
            data[str] = request.POST[str]

        # POST 값 임의 전송 방지
        data['status'] = 'WAIT'

        # script 태그작성 거부
        script_match = re.compile('(.*?)<script(.*?)>(.*?)</script>(.*?)', re.IGNORECASE) # 대소문자무시

        if script_match.match(data['contents']) is not None or script_match.match(data['title']) is not None:
            return Response(
                    # "script 태그는 사용할 수 없습니다."
                    data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00018)
                    , status=status.HTTP_400_BAD_REQUEST
                )

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)