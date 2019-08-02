from . import *


class SystemAlarmListView(ListAPIView):
    """
    시스템 메시지 전송 설정내용 가져오기
    """
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "system-alarm-list"
    permission_classes = [SystemAlarmViewPermission]
    queryset = SystemAlarm.objects.all()
    serializer_class = SystemAlarmSerializer
    #--------------------------------------
    #  METHODS
    #--------------------------------------
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        alarm_list = serializer.data
        data = {}

        for item in alarm_list:
            data[item['alarm_code']] = item

        return Response(data)