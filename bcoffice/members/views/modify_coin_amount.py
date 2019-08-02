from . import *


class ModifyCoinAmount(APIView):
    """
    코인수량 정정이력 생성
    """
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "modify-coin-amount"

    #--------------------------------------
    #  AUTHORITY
    #--------------------------------------
    permission_classes = [ModifyCoinAmountPermission]

    def get(self, request, *args, **kwargs):
        created_at = str(datetime.now())
        curreycy = request.query_params.get('currency', None)
        modify_type = request.query_params.get('modify_type', None)
        amount = request.query_params.get('amount', None)
        member_id = request.query_params.get('member_id', None)
        emp_no = User.objects.get(id = request.user.get_id()).emp_no
        comment = request.query_params.get('comment', None)

        if member_id is None:
            return Response(
                data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00017.format("member_id"))
                , status=status.HTTP_400_BAD_REQUEST
            )
        if curreycy is None:
            return Response(
                data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00017.format("curreycy"))
                , status=status.HTTP_400_BAD_REQUEST
            )
        if amount is None:
            return Response(
                data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00017.format('amount'))
                , status=status.HTTP_400_BAD_REQUEST
            )
        if modify_type is None:
            return Response(
                data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00017.format('modify_type'))
                , status=status.HTTP_400_BAD_REQUEST
            )
        if comment is None:
            return Response(
                data = ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00017.format('comment'))
                , status = status.HTTP_400_BAD_REQUEST
            )

        body = {
            "created_at": created_at,
            "curreycy": str(curreycy),
            "modify_type": modify_type,
            "amount": amount,
            "member_id": str(member_id),
            "emp_no": str(emp_no),
            "comment": str(comment)
        }
        params = {}
        params['member_id'] = member_id
        params['employee_id'] = emp_no
        params['currency'] = curreycy
        params['amount'] = amount

        if modify_type == "deposit":
            response = APIService.request_api(request, APIService.MEMBER_MODIFY_COIN_DEPOSIT, params)
        elif modify_type == "withdraw":
            response = APIService.request_api(request, APIService.MEMBER_MODIFY_COIN_WITHDRAW, params)

        log = CentralLogging()
        log.setLog(body, request, CREATE, response.status_code, 1200)

        # MONGO DB 추가
        logging_utils.set_log(TBL_BCOFFICE_MODIFY_COIN_AMOUNT, log.toJsonString())

        return response