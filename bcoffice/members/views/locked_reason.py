from . import *

class LockedReasonAPI(APIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "locked-reason"
    permission_classes = [LockedReasonAPIPermission]

    def get(self, request, *args, **kwargs):
        if request.query_params.get("markets", None) is None:
            return Response(data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00017.format("market")), status=status.HTTP_400_BAD_REQUEST)
        if request.query_params.get("currency", None) is None:
            return Response(data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00017.format("currency")), status=status.HTTP_400_BAD_REQUEST)
        if request.query_params.get("member_id", None) is None:
            return Response(data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00017.format("member_id")), status=status.HTTP_400_BAD_REQUEST)
        
        markets     = request.query_params.get("markets").split(",")
        currency    = request.query_params.get("currency")
        member_id   = request.query_params.get("member_id")

        # locked 상태 코드가 100 임
        # 일반주문 동결코인 수량
        orderSum = (
            Orders.objects.using("exchange").all()
            .filter(member_id=member_id)
            .filter(state=100)
            .filter(currency__in=markets)
            .aggregate(total = Sum('locked'))
        )

        # 스탑주문 동결코인 수량
        stopSum = (
            StopOrders.objects.using("exchange").all()
            .filter(member_id=member_id)
            .filter(state=100)
            .filter(currency__in=markets)
            .aggregate(total = Sum('locked'))
        )
        
        # 출금대기 동결코인 수량
        withdrawsSum = (
            Withdraws.objects.using("exchange").all()
            .exclude(aasm_state=constants.WithdrawAasmStateMap.data_map['DONE']['code'])
            .exclude(aasm_state=constants.WithdrawAasmStateMap.data_map['REJECTED']['code'])
            .exclude(aasm_state=constants.WithdrawAasmStateMap.data_map['CANCELED']['code'])
            .filter(member_id=member_id)
            .filter(currency=currency)
            .aggregate(total = Sum('sum'))
        )

        if orderSum['total'] is not None : order = orderSum["total"]
        else : order = 0

        if stopSum['total'] is not None : stop = stopSum["total"]
        else : stop = 0
        
        if withdrawsSum['total'] is not None : withdraw = withdrawsSum["total"]
        else : withdraw = 0
        
        result = {}
        result['order'] = order
        result['stop'] = stop
        result['withdraw'] = withdraw

        return Response(data=result, status=status.HTTP_200_OK)