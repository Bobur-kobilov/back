from . import *

# FAQ 상세 조회, 수정, 제거
class FaqDetailUpdateDestroy(RetrieveUpdateDestroyAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "faq-detail-update-destroy"
    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = FaqSerializer
        return serializer
    
    # 쿼리셋 가져오기
    def get_queryset(self):
        return Faq.objects.all()
    
    # 작성언어 시리얼라이징
    def get_lang_serializer(self, *args, **kwargs):
        serializer_class = FaqLanguageCreatedSerializer
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        lang = request.query_params.get('lang', None)
        serializer = self.get_serializer(instance)

        result = serializer.data
        if lang is not None:
            faq_category = FaqCategory.objects.values_list('category', flat = True).get(category_id = instance.faq_category_id, lang = lang)
            result['faq_category'] = faq_category

        return Response(result)

    # update 작성자가 맞는지 확인하기
    def update(self, request, *args, **kwargs):
        #--------------------------------------
        #  AUTHORITY
        #--------------------------------------
        permission_classes = [FaqUpdateDestroyPermission]

        instance = self.get_object()
        user_id = instance.user_id
        # url에서 pk 값 받은 후 해당 글의 작성자 확인
        if(user_id == request.user.get_id()):

            data = {}

            # session에서 user_id 가져오기
            data['user']            = request.user.get_id()
            data['faq_category_id'] = instance.faq_category_id
            data['title']           = instance.title
            data['contents']        = instance.contents

            for str in request.data :
                data[str] = request.data[str]

            # 참조키 값 업데이트
            instance.faq_category_id = data['faq_category_id']

            # title이나 contents 값이 빈 값이면 안됨
            if data['title'] is '' or data['contents'] is '':
                return Response(
                        # "제목이나 내용에 값이 없습니다."
                        data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00004)
                        , status=status.HTTP_400_BAD_REQUEST
                    )

            # script 태그작성 거부
            script_match = re.compile('(.*?)<script(.*?)>(.*?)</script>(.*?)', re.IGNORECASE) # 대소문자무시

            if script_match.match(data['contents']) is not None or script_match.match(data['title']) is not None:
                return Response(
                        # "script 태그는 사용할 수 없습니다."
                        data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00018)
                        , status=status.HTTP_400_BAD_REQUEST
                    )

            serializer = self.get_serializer(instance, data=data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()
            
            # lang값이 넘어오면 추가 제거 실행
            try:                
                # 해당 게시물 현재 DB에 반영된 선택된 언어 값 호출
                faq_language = list(FaqLanguage.objects.values().filter(board_id=instance.id))

                # 선택언어, 비선택언어 리스트 구분
                lang = data['lang'].split(',')
                lang_add = lang
                lang_remove = []
                for count in range(len(faq_language)):
                    # DB에 있는 값이 선택된 언어에 있으면 추가할 목록에서 제거
                    if faq_language[count]['lang'] in lang:
                        lang_add.remove(faq_language[count]['lang'])
                    # DB에 있는 값이 선택된 언어에 없으면 제거할 목록에 추가
                    else:
                        lang_remove.append(faq_language[count])

                # 제거 목록에 있는 값 DB에서 제거
                for count in range(len(lang_remove)):
                    faq_language = FaqLanguage.objects.filter(id=lang_remove[count]['id'])
                    self.perform_destroy(faq_language)
                
                # 추가 목록에 있는 값 DB에 추가
                lang_data = {}
                for count in range(len(lang_add)):
                    lang_data['board_id'] = instance.id
                    lang_data['lang'] = lang_add[count]
                    lang_serializer = self.get_lang_serializer(data=lang_data)
                    lang_serializer.is_valid(raise_exception=True)
                    lang_serializer.save()
            # lang값이 오지 않으면 전부 선택하지 않은 것이므로 전부 제거
            except:
                # 해당 게시물 현재 DB에 반영된 선택된 언어 값 호출
                faq_language = FaqLanguage.objects.filter(board_id=instance.id)
                # 제거
                self.perform_destroy(faq_language)

            return Response(serializer.data)
        else:
            return Response(
                    # "작성자와 일치하지 않습니다."
                    data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00003)
                    , status=status.HTTP_400_BAD_REQUEST
                )

    # delete 작성자가 맞는지 확인하기
    def destroy(self, request, *args, **kwargs):
        #--------------------------------------
        #  AUTHORITY
        #--------------------------------------
        permission_classes = [FaqUpdateDestroyPermission]

        # url에서 pk 값 받은 후 해당 글의 작성자 확인
        instance = self.get_object()
        user_id = instance.user_id
        if(user_id == request.user.get_id()):
            self.perform_destroy(instance)

            # 작성언어 제거
            faq_language = FaqLanguage.objects.filter(board_id=instance.id)
            self.perform_destroy(faq_language)

            return Response(
                    # "처리 되었습니다."
                    data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_INF00001)
                    , status=status.HTTP_204_NO_CONTENT
                )
        else:
            return Response(
                    # "작성자와 일치하지 않습니다."
                    data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00003)
                    , status=status.HTTP_400_BAD_REQUEST
                )