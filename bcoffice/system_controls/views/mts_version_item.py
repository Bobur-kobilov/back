from . import *

class MtsVersionItem(APIView):
    """
    MTS Version 아이템 가져오기
    """
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "mts-version-list"

    #--------------------------------------
    #  AUTHORITY
    #--------------------------------------
    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = MtsVersionSerializer
        return serializer

    def get_queryset(self, **kwargs):
        device = kwargs.get('device', None)

        if device is None :
            return None

        return MtsVersion.objects.get(device=device)

    def get(self, request, *args, **kwargs):
        device = request.query_params.get('device', None)

        if device is None :
            return Response(
                data = ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00017.format('device'))
                , status=status.HTTP_400_BAD_REQUEST
            )

        queryset = self.get_queryset(device = device)
        serializer = self.get_serializer_class()(queryset, many=False)
        return Response(data = serializer.data, status=status.HTTP_200_OK)