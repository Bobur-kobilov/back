from . import *


# 1:1 문의 수정, 제거 (거래소 API)
class QuestionUpdateDestroy(RetrieveUpdateDestroyAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "question-update-destroy"

    #--------------------------------------
    #  PROPERTIES : FILTER
    #--------------------------------------
    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = QuestionSerializer
        return serializer

    # 쿼리셋 가져오기
    def get_queryset(self):
        return Question.objects.all()

    def update(self, request, *args, **kwargs):
        #--------------------------------------
        #  AUTHORITY
        #--------------------------------------
        permission_classes = [QuestionUpdateDestroyPermission]

        instance = self.get_object()
        now_member_id = request.data['member_id']
        if(int(now_member_id) == int(instance.member_id)):

            # script 태그작성 거부
            script_match = re.compile('(.*?)<script(.*?)>(.*?)</script>(.*?)', re.IGNORECASE) # 대소문자무시

            if script_match.match(data['contents']) is not None or script_match.match(data['title']) is not None:
                return Response(
                        # "script 태그는 사용할 수 없습니다."
                        data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00018)
                        , status=status.HTTP_400_BAD_REQUEST
                    )

            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # delete 작성자가 맞는지 확인하기
    def destroy(self, request, *args, **kwargs):
        #--------------------------------------
        #  AUTHORITY
        #--------------------------------------
        permission_classes = [QuestionUpdateDestroyPermission]

        # url에서 pk 값 받은 후 해당 글의 작성자 확인
        instance = self.get_object()
        member_id = instance.member_id
        now_member_id = request.data['member_id']
        if(int(member_id) == int(now_member_id)):
            # 글 제거
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)