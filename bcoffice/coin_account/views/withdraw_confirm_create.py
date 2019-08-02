from . import *
from bcoffice.logging import CentralLogging
from bcoffice.utils import logging_utils

ACTION_CREATE = 'CREATE'
SCREEN_CUSTOMER_WITHDRAWALS_LIST = 3230
RESULT_SUCCESS = 'success'


# 암호화폐 출금 승인
class WithdrawConfirmCreate(CreateAPIView):
    # --------------------------------------
    #  PROPERTIES
    # --------------------------------------
    name = "withdraw-confirm-create"

    # --------------------------------------
    #  AUTHORITY
    # --------------------------------------
    permission_classes = [ManualWithdrawConfirmePermission]

    # --------------------------------------
    #  OVERRIDEN METHODS
    # --------------------------------------

    # 암호화폐 출금 승인
    def post(self, request, *args, **kwargs):
        response = {
            "data": {}
        }
        if request.data['withdraw_id'] is not None:
            for item in request.data:
                response['data'][item] = request.data[item]

            mq_utils.request_withdraw(str(response['data']['withdraw_id']))

            response['data']['result'] = RESULT_SUCCESS
            response['status'] = status.HTTP_201_CREATED
            response['headers'] = self.get_success_headers(response['data'])
        else:
            response['data'] = ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00017.format('withdraw_id'))
            response['status'] = status.HTTP_400_BAD_REQUEST

        log = CentralLogging() \
            .setLog(response['data'], request, ACTION_CREATE, response['status'], SCREEN_CUSTOMER_WITHDRAWALS_LIST)
        logging_utils.set_log(TBL_BCOFFICE_WITHDRAW_CONFIRM, log.toJsonString())

        return Response(**response)

# def create(self, request, *args, **kwargs):

#    data = {}
#    for item in request.data:
#        data[item] = request.data[item]

#    withdraw_id = data['withdraw_id']
#    if withdraw_id is None:
#        return Response(
#            data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00017.format("withdraw_id"))
#            , status=status.HTTP_400_BAD_REQUEST)

#    mq_utils.request_withdraw(str(withdraw_id))

#    data['result'] = 'success'
#    headers = self.get_success_headers(data)

#    return Response(data, status=status.HTTP_201_CREATED, headers=headers)
