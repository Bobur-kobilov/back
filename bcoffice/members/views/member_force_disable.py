from . import *
import pytz

# 회원 강제 상태변경
class MemberForceDisable(APIView):
    name = "member-force-disable"
    permission_classes = [MemberForceDisablePermission]
        
    def put(self, request, *args, **kwargs):
        member_id = request.data.get('member_id', None)
        reason = request.data.get('reason', None)
        authType = request.data.get('authType', None)
        if member_id is None:
            return Response( # "{0} 파라미터가 없습니다."
                data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00017.format('member_id'))
                , status=status.HTTP_400_BAD_REQUEST
            )
        auth_type = None
        request_after = None
        if authType == 'factor_auth':
            auth_type = request.data.get('auth_type', None)
            if auth_type is None:
                return Response( # "{0} 파라미터가 없습니다."
                    data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00017.format('auth_type'))
                    , status=status.HTTP_400_BAD_REQUEST
                )
        else:
            request_after = request.data.get('after', None)
            if request_after is None:
                return Response( # "{0} 파라미터가 없습니다."
                    data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00017.format('after'))
                    , status=status.HTTP_400_BAD_REQUEST
                )
        
        category = ""
        if authType == 'factor_auth':
            factor_type = ""
            if auth_type == 'app':
                category = "OTP 인증해제"
                factor_type = "TwoFactor::App"
            elif auth_type == 'sms':
                category = "SMS 인증해제"
                factor_type = "TwoFactor::Sms"
            before = (TwoFactors.objects.using("exchange").filter(member_id=member_id).filter(type=factor_type))[0].activated
            after = int(not before)
        else:
            VALUE_BY_TYPE = {
                'kyc_auth' : {'category': '신분증 인증', 'db_column': 'kyc_activated'},
                'disable': {'category': '계정비활성화', 'db_column': 'disabled'},
                'restrict': {'category': '이용제한', 'db_column': 'restricted'},
                'deleted': {'category': '회원탈퇴', 'db_column': 'deleted'},
            }
            category = VALUE_BY_TYPE[authType]['category']
            column = VALUE_BY_TYPE[authType]['db_column']
            before = Members.objects.using("exchange").values(column).get(id=member_id)[column]
            after = request_after
            if before == after:
                return Response( # "현재상태와 변경하려는 상태가 동일합니다."
                    data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00032)
                    , status=status.HTTP_400_BAD_REQUEST
                )

        user = User.objects.get(id=request.user.get_id())

        body = {
            "user_id": request.user.get_id()
            , "emp_no": user.emp_no
            , "member_id": int(member_id)
            , "category": category
            , "before": before
            , "after": after
            , "reason": reason
            , "created_at": str(datetime.now(pytz.timezone('Asia/Seoul')))
        }

        API_BY_TYPE = {
            'factor_auth': {'api': APIService.MEMBER_TWO_FACTOR, 'params': {'member_id': member_id, 'auth_type': auth_type}},
            'kyc_auth': {'api': APIService.MEMBER_KYC_AUTH, 'params': {'member_id': member_id, 'active': request_after}},
            'disable': {'api': APIService.MEMBER_DISABLE, 'params': {'member_id': member_id, 'disable': request_after}},
            'restrict': {'api': APIService.MEMBER_RESTRICT, 'params': {'member_id': member_id, 'restrict': request_after}},
            'deleted': {'api': APIService.MEMBER_DELETED, 'params': {'member_id': member_id}},
        }
        response = APIService.request_api(request, API_BY_TYPE[authType]['api'], API_BY_TYPE[authType]['params'])

        log = CentralLogging()
        log.setLog(body, request, UPDATE, response.status_code, 1200)

        # MONGO DB 추가
        # body = json.dumps(log).encode('utf8')
        logging_utils.set_log(TBL_BCOFFICE_MEMBER_MOD, log.toJsonString())

        return response