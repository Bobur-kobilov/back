from . import *


# 코인가이드 목록 상세 조회, 수정, 삭제
class CoinGuideDetailUpdateDestroy(RetrieveUpdateDestroyAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "coinguide-detail-update-destroy"
    
    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = CoinGuideSerializer
        return serializer
    
    # 쿼리셋 가져오기
    def get_queryset(self):
        return CoinGuide.objects.all()
    
    # 작성언어 시리얼라이징
    def get_lang_serializer(self, *args, **kwargs):
        serializer_class = CoinGuideLanguageCreateSerializer
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance    = self.get_object()
        serializer  = self.get_serializer(instance)
        return Response(serializer.data)

    # update 작성자가 맞는지 확인하기
    def update(self, request, *args, **kwargs):
        #--------------------------------------
        #  AUTHORITY
        #--------------------------------------
        permission_classes = [CoinGuideUpdateDestroyPermission]
        
        instance = self.get_object()

        # url에서 pk 값 받은 후 해당 글의 작성자 확인
        user_id = instance.user_id

        if(user_id == request.user.get_id()):
            # UPDATE 시 값 임의 전송 방지
            data = {}
            data['status'] = instance.status

            for str in request.data :
                data[str] = request.data[str]
            
            # script 태그작성 거부
            script_match = re.compile('(.*?)<script(.*?)>(.*?)</script>(.*?)', re.IGNORECASE) # 대소문자무시

            if script_match.match(data['contents']) is not None or script_match.match(data['title']) is not None:
                return Response(
                        # "script 태그는 사용할 수 없습니다."
                        data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00018)
                        , status=status.HTTP_400_BAD_REQUEST
                    )
                    
            # type이 ing나 active이어야 함 (ing : 작성중 / active : 작성완료)
            status_type = ['ing', 'active']
            if not data['status'] in status_type:
                return Response (
                        # "status값을 'ing', 'active'로 설정해 주세요."
                        data    = ResponseMessage.getMessageDwata(ResponseMessage.MESSAGE_ERR00009)
                        ,status = status.HTTP_400_BAD_REQUEST
                    )
            data['user']        = request.user.get_id()

            serializer = self.get_serializer(instance, data=data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()
            
            # lang값이 넘어오면 추가 제거 실행
            try:
                # 해당 게시물 현재 DB에 반영된 선택된 언어 값 호출
                coinguide_language = list(CoinGuideLanguage.objects.values().filter(board_id=instance.id))

                # 선택언어, 비선택언어 리스트 구분
                lang = data['lang'].split(',')
                lang_add = lang
                lang_remove = []
                for count in range(len(coinguide_language)):
                    # DB에 있는 값이 선택된 언어에 있으면 추가할 목록에서 제거
                    if coinguide_language[count]['lang'] in lang:
                        lang_add.remove(coinguide_language[count]['lang'])
                    # DB에 있는 값이 선택된 언어에 없으면 제거할 목록에 추가
                    else:
                        lang_remove.append(coinguide_language[count])

                # 제거 목록에 있는 값 DB에서 제거
                for count in range(len(lang_remove)):
                    coinguide_language = CoinGuideLanguage.objects.filter(id=lang_remove[count]['id'])
                    self.perform_destroy(coinguide_language)
                
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
                coinguide_language = CoinGuideLanguage.objects.filter(board_id=instance.id)
                # 제거
                self.perform_destroy(coinguide_language)

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
        permission_classes = [CoinGuideUpdateDestroyPermission]

        instance = self.get_object()
        # url에서 pk 값 받은 후 해당 글의 작성자 확인
        user_id = instance.user_id
        if(user_id == request.user.get_id()):
            # 로고 제거
            coinguide_logo = CoinGuide.objects.filter(id = instance.id)
            coinguide_logo_id = None
            for obj in coinguide_logo:
                coinguide_logo_id = obj.logo_id
            file_logo = FileAttachment.objects.filter(id = coinguide_logo_id)
            file_logo.delete()

            # 글 제거
            self.perform_destroy(instance)
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