from . import *


# 공지사항 상세 조회, 수정, 삭제
class NoticeDetailUpdateDestroy(RetrieveUpdateDestroyAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "notice-detail-update-destroy"
    
    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = NoticeSerializer
        return serializer
    
    # 쿼리셋 가져오기
    def get_queryset(self):
        return Notice.objects.all()
    
    # 작성언어 시리얼라이징
    def get_lang_serializer(self, *args, **kwargs):
        serializer_class = NoticeLanguageCreateSerializer
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        #--------------------------------------
        #  AUTHORITY
        #--------------------------------------
        # permission_classes = [NoticeDetailPermission]
        
        instance    = self.get_object()
        serializer  = self.get_serializer(instance)

        # 거래소 언어선택 값
        selected_lang = request.query_params.get('lang', '')
        if selected_lang is not None and selected_lang is not '':
            selected_lang = " AND l.lang = '{0}'".format(selected_lang)

        # 이전글, 다음글 가져오기
        query = """
            SELECT 
                bn.id
                , title
            FROM
                boards_notice as bn
            LEFT JOIN
                boards_notice_language as bnl
            ON
                bn.id = bnl.board_id
            WHERE
                bn.id IN ( 
                    (SELECT n.id FROM boards_notice n 
                        LEFT JOIN boards_notice_language
                            AS l ON n.id = l.board_id
                        WHERE n.id < {0} AND status = 'active'{1}
                        ORDER BY n.id DESC LIMIT 1),
                    (SELECT n.id FROM boards_notice n
                        LEFT JOIN boards_notice_language
                            AS l ON n.id = l.board_id
                        WHERE n.id > {0} AND status = 'active'{1}
                        ORDER BY n.id LIMIT 1)
                )
            GROUP BY bn.id
        """.format(instance.id, selected_lang)

        # 이전글, 다음글 값 array에 붙이기
        queryset = Notice.objects.raw(query)
        result_val = []
        for obj in queryset:
            result_val.append({'id':obj.id, 'title':obj.title})

        result_data = {}
        for str in serializer.data:
            result_data[str] = serializer.data[str]
        
        # 이전글, 다음글이 없는 경우 처리
        result_data['pre']  = None
        result_data['next'] = None
        for i in range(len(result_val)):
            if int(result_val[i]['id']) < instance.id:
                result_data['pre'] = result_val[i]
            else:
                result_data['next'] = result_val[i]
        
        return Response(result_data)

    # update 작성자가 맞는지 확인하기
    def update(self, request, *args, **kwargs):
        #--------------------------------------
        #  AUTHORITY
        #--------------------------------------
        permission_classes = [NoticeUpdateDestroyPermission]

        instance = self.get_object()

        # url에서 pk 값 받은 후 해당 글의 작성자 확인
        user_id = instance.user_id

        if (user_id == request.user.get_id()):
            # UPDATE 시 값 임의 전송 방지
            data = {}
            # 작성상태 체크
            data['status']  = instance.status
            data['media']   = None

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
                        data    = ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00009)
                        ,status = status.HTTP_400_BAD_REQUEST
                    )
            data['user']        = request.user.get_id()
            data['read_count']  = instance.read_count

            # 메일 및 문자는 초기 한번만 전송되야함.
            # send 값이 False 였다가 True가 되면 알림 발송
            transfer_method = ['sms', 'mail']

            media_list = []
            if data['media'] is not None:
                media_list = data['media'].split(',')
            
            # 리스트 중복제거
            media_list = list(set(media_list))

            # 전송유무를 db에서 확인 후
            check_send_email    = instance.send_email
            check_send_sms      = instance.send_sms
            
            for media in media_list:
                if media in transfer_method and data['status'] == 'active':
                    # 메일 발송 및 로그 저장
                    user_id     = request.user.get_id()
                    contents    = data['contents']
                    if media == 'mail' and not instance.send_email:
                        # 전체회원 이메일 목록
                        email_list = Members.objects.using('exchange').values_list('email', flat=True)
                        
                        title       = data['title']

                        SendMail.send(
                            sender_id   = user_id,
                            target_list = email_list,
                            title       = title,
                            contents    = contents)
                        
                        # 전송을 하면 전송했다고 저장
                        check_send_email = True
                    # 문자 발송 및 로그 저장
                    elif media == 'sms' and not instance.send_sms:
                        # p태그 제거 및 개행으로 변경
                        contents = re.sub(re.compile('<p?>', re.IGNORECASE), '', contents)
                        contents = re.sub(re.compile('<(.*?)/p(.*?)>', re.IGNORECASE), '\n', contents)

                        # br태그 개행으로 변경
                        contents = re.sub(re.compile('<(.*?)br(.*?)>', re.IGNORECASE), '\n', contents)

                        # 남은 태그들 제거
                        contents = re.sub(re.compile('<.*?>', re.IGNORECASE), '', contents)

                        # 전체 회원 전화번호 목록
                        phone_list = list(Members.objects.using('exchange').filter(disabled=0).exclude(phone_number__isnull=True).exclude(phone_number__exact='').values_list('phone_number', flat=True))
                        
                        SendSMS.send(
                            sender_id       = user_id
                            , target_list   = phone_list
                            , message       = contents
                        )
                        
                        # 전송을 하면 전송했다고 저장
                        check_send_sms = True

            # 전송했는지 안했는지를 파악 후 전송했으면 True인 값 저장
            # 전송을 하지 않았으면 db값 그대로 다시 저장
            data['send_email'] = check_send_email
            data['send_sms'] = check_send_sms

            serializer = self.get_serializer(instance, data=data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()
            
            # lang값이 넘어오면 추가 제거 실행
            try:                
                # 해당 게시물 현재 DB에 반영된 선택된 언어 값 호출
                notice_language = list(NoticeLanguage.objects.values().filter(board_id=instance.id))

                # 선택언어, 비선택언어 리스트 구분
                lang = data['lang'].split(',')
                lang_add = lang
                lang_remove = []
                for count in range(len(notice_language)):
                    # DB에 있는 값이 선택된 언어에 있으면 추가할 목록에서 제거
                    if notice_language[count]['lang'] in lang:
                        lang_add.remove(notice_language[count]['lang'])
                    # DB에 있는 값이 선택된 언어에 없으면 제거할 목록에 추가
                    else:
                        lang_remove.append(notice_language[count])

                # 제거 목록에 있는 값 DB에서 제거
                for count in range(len(lang_remove)):
                    notice_language = NoticeLanguage.objects.filter(id=lang_remove[count]['id'])
                    self.perform_destroy(notice_language)
                
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
                notice_language = NoticeLanguage.objects.filter(board_id=instance.id)
                # 제거
                self.perform_destroy(notice_language)

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
        permission_classes = [NoticeUpdateDestroyPermission]

        instance = self.get_object()
        # url에서 pk 값 받은 후 해당 글의 작성자 확인
        user_id = instance.user_id
        if(user_id == request.user.get_id()):
            # 첨부파일 제거
            notice_normal_id = None
            notice_map = NoticeFileMap.objects.filter(board_id = instance.id)
            for obj in notice_map:
                notice_normal_id = obj.file_info_id
                file_normal = FileAttachment.objects.filter(id = notice_normal_id)
                file_normal.delete()
            notice_map.delete()

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