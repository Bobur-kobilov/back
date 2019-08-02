class ResponseMessage :
    MESSAGE_ERR00001 = "status값이 없습니다." "status값이 없습니다"
    MESSAGE_ERR00002 = "상태값을 변경하기 위해서는 답변을 작성해야합니다."
    MESSAGE_ERR00003 = "작성자와 일치하지 않습니다."
    MESSAGE_ERR00004 = "제목이나 내용에 값이 없습니다."
    MESSAGE_ERR00005 = "작성자가 일치하지 않거나 게시물의 위치가 올바르지 않습니다."
    MESSAGE_ERR00006 = "type을 'normal', 'primary'로 설정해 주세요."
    MESSAGE_ERR00007 = "회원검색 값을 넣어주세요."
    MESSAGE_ERR00008 = "일치하는 값이 없습니다."
    MESSAGE_ERR00009 = "status값을 'ing', 'active'로 설정해 주세요."
    MESSAGE_ERR00010 = "삭제 되었습니다."
    MESSAGE_ERR00011 = "limit, offset 값을 넣어주세요."
    MESSAGE_ERR00012 = "ID를 숫자형식으로 입력해주세요."
    MESSAGE_ERR00013 = "조회기간을 선택해주세요."
    MESSAGE_ERR00014 = "카테고리를 선택해주세요."
    MESSAGE_ERR00015 = "사용자 ID 또는 권한 값이 없습니다."
    MESSAGE_ERR00016 = "삭제할 수 없습니다."
    MESSAGE_ERR00017 = "{0} 파라미터가 없습니다."
    MESSAGE_ERR00018 = "script 태그는 사용할 수 없습니다."
    MESSAGE_ERR00019 = "일주일 기간내의 기간을 선택해주세요."
    MESSAGE_ERR00020 = "이미지 파일을 첨부해주세요."
    MESSAGE_ERR00021 = "일치하는 currency 값이 없습니다."
    MESSAGE_ERR00022 = "검색된 회원이 없습니다."
    MESSAGE_ERR00023 = "보안등급 레벨이 잘못되었습니다."
    MESSAGE_ERR00024 = "{0} 코인의 정보를 가져올 수 없습니다. 코인노드를 확인해주세요."
    MESSAGE_ERR00025 = "코인을 송금하던 도중 오류가 발생했습니다. 확인 후 다시 전송해주세요."
    MESSAGE_ERR00026 = "이미 처리가 완료된 출금요청입니다."
    MESSAGE_ERR00027 = "지갑잔고보다 출금요청된 수량이 더 많습니다."
    MESSAGE_ERR00028 = "현재 비밀번호가 일치하지 않습니다."
    MESSAGE_ERR00029 = "권한이 없습니다."
    MESSAGE_ERR00030 = "요청한 코인 ID와 일치하는 코인이 존재하지 않습니다."
    MESSAGE_ERR00031 = "요청한 ID와 일치하는 출금내역이 존재하지 않습니다."
    MESSAGE_ERR00032 = "현재상태와 변경하려는 상태가 동일합니다."
    MESSAGE_ERR00033 = "날짜 확인해주세요"
    MESSAGE_ERR00034 = "데이터베이스 연결 오류"

    MESSAGE_INF00001 = "처리되었습니다."
    MESSAGE_INF00002 = "수정하였습니다."
    
    def getMessageData( message, *args, **kwargs ):
        if kwargs.get('param', None):
            msg = message.format(kwargs.get('param'))
        else :
            msg = message
            
        data = {
            "message": msg
        }

        return data