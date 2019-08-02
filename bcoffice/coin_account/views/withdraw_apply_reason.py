from . import *

class WithdrawApplyReason(ListAPIView):
    name = "withdraw_apply_reason"
    permission_classes = [WithdrawApplyReasonPermission]

    def get_serializer_class(self):
        serializer = WithdrawReasonSerializer
        return serializer

    def get_queryset(self, *args, **kwargs):
        queryset = WithdrawReason.objects.all()

        reason_type = kwargs.get("reason_type", None)

        queryset = queryset.filter(reason_type__contains=reason_type)
        queryset = queryset.order_by("code")
        return queryset

    def list(self, request, *args, **kwargs):
        reason_type   = request.query_params.get('reason_type', None)

        if reason_type is None:
            return Response(
                data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00017.format("reason_type"))
                , status=status.HTTP_400_BAD_REQUEST)

        queryset = self.get_queryset(
            reason_type = reason_type
        )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)