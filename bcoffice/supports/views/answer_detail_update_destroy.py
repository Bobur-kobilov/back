from . import *


# 1:1 답변 내역 상세조회, 수정, 삭제
class AnswerDetailUpdateDestroy(RetrieveUpdateDestroyAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "answer-detail-update-destroy"

    #--------------------------------------
    #  AUTHORITY
    #--------------------------------------
    permission_classes = [AnswerDetailUpdateDestroyPermission]

    #--------------------------------------
    #  ANSWER TARGET TO QUESTION
    #--------------------------------------
    lookup_field = 'target'

    #--------------------------------------
    #  PROPERTIES : FILTER
    #--------------------------------------
    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = AnswerSerializer
        return serializer

    # 쿼리셋 가져오기
    def get_queryset(self):
        return Answer.objects.all()

    # update 작성자가 맞는지 확인하기
    def update(self, request, *args, **kwargs):
        # url에서 pk 값 받은 후 해당 글의 작성자 확인
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # UPDATE 시 값 임의 전송 방지
        data = {}
        for str in request.data :
            data[str] = request.data[str]

        data['user'] = request.user.get_id()
        data['target'] = Question.objects.values_list('id', flat=True).get(id=kwargs['target'])

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    # delete 작성자가 맞는지 확인하기
    def destroy(self, request, *args, **kwargs):
        # url에서 pk 값 받은 후 해당 글의 작성자 확인
        # 질문에 대한 처리상태 '대기'
        queryset = Question.objects.filter(id=kwargs['target'])
        queryset.update(status='WAIT')

        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)