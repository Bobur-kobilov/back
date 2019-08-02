from django.conf import settings
from rest_framework             import status
from rest_framework.response    import Response
import requests

class APIService:
    # API URL 리스트
    
    # 등급별 출금한도 설정 (POST - level : 등급, amount : 수량)
    WITHDRAW_LIMIT_SET = '/api/v2/backoffice/withdraw_limit'

    # 추천인 수수료 조회 / 수정 (GET - member_id, POST - fee : 수수료, member_id : 회원번호)
    REFERRAL_FEE_SET = '/api/v2/backoffice/referral/member'
    
    # 추천인 정책 수수료 수정 (POST - fee : 수수료)
    REFERRAL_POLICY_FEE_SET = '/api/v2/backoffice/referral/policy'

    # 회원 SMS 인증 등록 해제(PUT - member_id, active(0, 1))
    MEMBER_TWO_FACTOR = '/api/v2/backoffice/member_managements/disable_two_factor'

    # 회원 신분증 인증 등록 해제(PUT - member_id, active(0, 1))
    MEMBER_KYC_AUTH = '/api/v2/backoffice/member_managements/kyc_auth'

    # 회원탈퇴(PUT - member_id, disable(0, 1))
    MEMBER_DISABLE = '/api/v2/backoffice/member_managements/member_disable'

    # 회원 이용제한(PUT - member_id, restrict(0, 1))
    MEMBER_RESTRICT = '/api/v2/backoffice/member_managements/member_restrict'

    MEMBER_DELETED = '/api/v2/backoffice/member_managements/delete_member'

    # 1:1 문의 답변완료 호출 API(GET - member_id, board_id, locale(ko, en, fr))
    MEMBER_QNA_ANSWER = '/api/v2/backoffice/member_managements/qna_answer'

    # 회원 코인 원장입금 API(GET - parameter : member_id, employee_id, currency, amount)
    MEMBER_MODIFY_COIN_DEPOSIT = '/api/v2/backoffice/force_deposit'

    # 회원 코인 원장출금 API(GET - parameter : member_id, employee_id, currency, amount)
    MEMBER_MODIFY_COIN_WITHDRAW = '/api/v2/backoffice/force_withdraw'

    # 주문내역 강제취소 API(GET - parameter : member_id, employee_id, id)
    MEMBER_ORDER_FORCE_CANCEL = '/api/v2/backoffice/force_cancel_order'

    # 수동출금처리 취소 API(GET - parameter : withdraw_id)
    MEMBER_WITHDRAW_CANCEL = '/api/v2/backoffice/force_withdraw_cancel'

    # MANUAL WITHDRAW CONFIRM
    MANUAL_WITHDRAW_CONFIRM = '/api/v2/backoffice/force_withdraw_confirm'

    METHOD_MAP = {
        'GET'       : requests.get
        , 'POST'    : requests.post
        , 'PUT'     : requests.put
        , 'DELETE'  : requests.delete
    }

    """
    API 요청 메서드
    @param request API 요청 request 객체
    @param url API URL 주소
    @param params API 호출시 전송할 파라미터 값들(Dictonary)
    @return Response
    """
    def request_api(request, url = None, params = None, *args, **kwargs):
        headers = {}
        url = settings.API_PROTOCOL + '://' + settings.API_HOST + url
        method = request.method.upper()

        result = APIService.METHOD_MAP[method](url, params=params)
        return Response(data = result.json(), status = status.HTTP_200_OK)

    def request(url = None, params = None, *args, **kwargs ):
        if url.find("://") > -1:
            pass
        else :
            url = settings.API_PROTOCOL + '://' + settings.API_HOST + url

        return requests.get(url, params = params).json()


    def rpc_call(url = None, params = None, method = None, is_json = False, timeout = None):
        request_func = APIService.METHOD_MAP[method.upper()]
        response = None

        if method == 'get' :
            if timeout is None :
                response = request_func(url, params = params)
            else :
                response = request_func(url, params = params, timeout=timeout)
        elif method == 'post' :
            if is_json :
                if timeout is None :
                    response = request_func(url, json = params)
                else :
                    response = request_func(url, json = params, timeout=timeout)
            else :
                if timeout is None :
                    response = request_func(url, data = params)
                else :
                    response = request_func(url, data = params, timeout=timeout)
        elif method == 'put' : 
            if timeout is None :
                response = request_func(url, data = params)
            else :
                response = request_func(url, data = params, timeout=timeout)
        elif method == 'delete':
            if timeout is None :
                response = request_func(url)
            else :
                response = request_func(url, timeout=timeout)
                
        return response.json()
        