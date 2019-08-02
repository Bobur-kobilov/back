from . import *


# 1:1 문의 내역 상세 조회 / 답변 처리상태 변경
class QuestionDetailUpdate(RetrieveUpdateAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "question-detail-update"
    permission_classes = [QuestionDetailPermission]
    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = QuestionStateSerializer
        return serializer

    # 쿼리셋 가져오기
    def get_queryset(self):
        return Question.objects.all()

    def retrieve(self, request, *args, **kwargs):

        lang = request.query_params.get('lang', None)

        instance = self.get_object()
        serializer = self.get_serializer(instance)

        data = Members.objects.using('exchange').values('display_name','email', 'phone_number').filter(id=serializer.data['member_id'])[0]
        result = serializer.data
        if lang is not None:
            category = QuestionType.objects.values_list('type', flat = True).get(category_id = instance.question_type_id, lang=lang)
            result['question_type'] = category

        result['member_name']   = data['display_name']
        result['member_email']  = data['email']
        result['member_phone']  = data['phone_number']

        return Response(result)

    def update(self, request, *args, **kwargs):

        answer = None
        instance = self.get_object()
        question_type_id = request.data.get("question_type_id", None)

        # 상태 값이 WAIT(대기중)에서 PROC로 넘어가는 경우 Answer에 레코드를 추가한다.
        # 상태 값이 WAIT(대기중)에서 바로 CPLT로 넘어가는 경우 Answer에 레코드가 존재해야만 한다.
        # 상태 값이 WAIT(대기중)에서 바로 CPLT로 넘어가는 경우 Answer에 레코드가 존재하는 경우 contents 필드에 값이 있어야만 한다.
        # 상태 값이 PROC(처리중)에서 CPLT로 넘어가는 경우도 마찬가지다.
        # 나머지 경우 상태 값만 변경
        try :
            answer = Answer.objects.get(target_id=kwargs['pk'])
        except :
            # Answer 객체가 없을 수도 있기 때문에 try - except로 처리
            pass

        if request.data['status'] :
            question_status = request.data['status']
        else :
            return Response(
                    data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00001)
                    , status=status.HTTP_400_BAD_REQUEST
                )

        if instance.status == 'WAIT' and question_status == 'PROC' and not answer:
            Answer.objects.create(
                user_id=request.user.get_id()
                , target_id=instance.id
                , locale='ko'
            )
        elif (
                ( instance.status == 'WAIT' and question_status == 'CPLT' ) or
                ( instance.status == 'PROC' and question_status == 'CPLT' )
            ) and ( not answer or not answer.contents or answer.contents.__len__() == 0  ) :
            return Response(
                    data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00002)
                    , status=status.HTTP_400_BAD_REQUEST
                )

        if ( instance.status != question_status ):
            answer_instance = Answer.objects.get(target_id = instance.id)
            answer_instance.user_id = request.user.get_id()
            answer_instance.save()

        data = {}

        data['member_id']       = instance.member_id
        data['question_type']   = 'instance.question_type'
        data['status']          = instance.status
        data['title']           = instance.title
        data['contents']        = instance.contents
        data['status']          = question_status
        data['question_type_id'] = question_type_id

        serializer = self.get_serializer(instance, data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        

        if question_status == 'CPLT':
            params = {}
            params['member_id'] = instance.member_id
            params['board_id'] = instance.id
            params['locale'] = answer.locale
            params['question_type_id'] = question_type_id

            result = APIService.request(APIService.MEMBER_QNA_ANSWER, params)
        return Response(serializer.data)