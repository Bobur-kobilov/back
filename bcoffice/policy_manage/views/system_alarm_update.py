from . import *


class SystemAlarmUpdateView(APIView):
    """
    시스템 메시지 전송 설정 수정
    """
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "system-alarm-update"
    permission_classes = [SystemAlarmUpdateViewPermission]
    #--------------------------------------
    #  METHODS
    #--------------------------------------
    def put(self, request, *args, **kwargs):
        alarm_list = request.data.get("alarm_list", None)

        if alarm_list is None:
            return Response(
                data = ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00017.format("alarm_list")
                , status = status.HTTP_400_BAD_REQUEST )
            )

        alarm_data = json.loads(alarm_list)

        for data in alarm_data:
            item = alarm_data[data]
            instance = SystemAlarm.objects.get(pk=item['id'])
            instance.is_sms = item['is_sms']
            instance.is_email = item['is_email']
            instance.save()

        return Response(status=status.HTTP_200_OK)