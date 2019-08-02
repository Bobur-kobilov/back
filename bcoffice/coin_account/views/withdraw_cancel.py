from . import *

class WithdrawCancel(APIView):
    # --------------------------------------
    #  PROPERTIES
    # --------------------------------------
    name = "withdraw-cancel"
    # permission_classes = [ManualWithdrawConfirmePermission]

    def post(self, request, *args, **kwargs):
        created_at = str(datetime.now())
        withdraw_id = request.data.get('withdraw_id', None)
        employee_id = User.objects.get(id = request.user.get_id()).emp_no
        reason = request.data.get('reason', None)

        body = {
            "created_at": created_at,
            "withdraw_id": int(withdraw_id),
            "employee_id": int(employee_id),
            'reason': reason
        }
        params = {
            'withdraw_id': withdraw_id
        }

        request.method = 'get'
        response = APIService.request_api(request, APIService.MEMBER_WITHDRAW_CANCEL, params)

        log = CentralLogging()
        log.setLog(body, request, CREATE, response.status_code, 3280)

        # MONGO DB 추가
        logging_utils.set_log(TBL_BCOFFICE_WITHDRAW_CANCEL, log.toJsonString())

        return response