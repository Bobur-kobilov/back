from . import *

class SystemAlarmItemView(APIView):
    """
    시스템 메시지 전송방식 아이템 가져오기
    """
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "system-alarm-item"
    serializer_class = SystemAlarmSerializer
    #--------------------------------------
    #  METHOD
    #--------------------------------------
    def get(self, request, *args, **kwargs):
        alarm_code = request.query_params.get("alarm_code", None)

        if alarm_code is None:
            return Response(
                data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00017.format("alarm_code"))
                , status=status.HTTP_400_BAD_REQUEST
            )

        item = SystemAlarm.objects.get(alarm_code = alarm_code)
        serializer = self.serializer_class(item, many=False)

        return Response(data=serializer.data, status=status.HTTP_200_OK)