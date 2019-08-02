from . import *


# 주문내역 강제취소
class OrderForceCancel(APIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "order-force-cancel"

    #--------------------------------------
    #  AUTHORITY
    #--------------------------------------
    permission_classes = [OrderForceCancelPermission]

    def get(self, request, *args, **kwargs):
        created_at = str(datetime.now())

        member_id = request.query_params.get('member_id', None)
        employee_id = User.objects.get(id = request.user.get_id()).emp_no
        order_id = request.query_params.get('order_id', None)

        body = {
            "created_at": created_at,
            "member_id":    int(member_id),
            "order_id":     int(order_id),
            "employee_id":  int(employee_id),
        }

        params = {}
        params['member_id'] = member_id
        params['employee_id'] = employee_id
        params['id'] = order_id

        response = APIService.request_api(request, APIService.MEMBER_ORDER_FORCE_CANCEL, params)

        log = CentralLogging()
        log.setLog(body, request, CREATE, response.status_code, 2100)

        # MONGO DB 추가
        logging_utils.set_log(TBL_BCOFFICE_ORDER_FORCE_CANCEL, log.toJsonString())

        return response