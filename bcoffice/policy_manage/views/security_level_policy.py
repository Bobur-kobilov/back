from . import *

class SecurityLevelPolicy(APIView):
    """
    입출금 한도관리
    """
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "security-level-policy"
    permission_classes = [SecurityLevelPolicyPermission]

    #--------------------------------------
    #  METHODS
    #--------------------------------------
    def get(self, request, *args, **kwargs):
        return APIService.request_api(request=request, url=APIService.WITHDRAW_LIMIT_SET)

    def post(self, request, *args, **kwargs):
        if request.data.get('level', False):
            param = {}
            param['level'] = request.data.get('level')
            param['amount'] = request.data.get('amount')

            original = APIService.request(request=request, url=APIService.WITHDRAW_LIMIT_SET)
            original_item = None

            for item in original:
                if item['level'] == int(param['level']):
                    original_item = item
                    break

            if item is None:
                return Response(
                    data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00023)
                    , status=status.HTTP_400_BAD_REQUEST
                )

            user = User.objects.get(id = request.user.get_id())

            body = {
                "user_id"       : request.user.get_id()
                , "emp_no"      : user.emp_no
                , "level" : int(param['level'])
                , "before": float(original_item['amount'])
                , "after" : float(param['amount'])
                , "created_at"  : str(datetime.now())
            }

            response = APIService.request_api(request=request, url=APIService.WITHDRAW_LIMIT_SET, params=param)

            log = CentralLogging()
            log.setLog(body, request, UPDATE, response.status_code, 4120)

            # MONGO DB 추가
            # body = json.dumps(log).encode('utf8')
            logging_utils.set_log(TBL_BCOFFICE_DEPOSIT_WITHDRAW_MOD, log.toJsonString())

            return response

        return Response(
                data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00017, param='level 또는 amount')
                , status=status.HTTP_400_BAD_REQUEST
            )