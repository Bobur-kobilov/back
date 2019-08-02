from . import *

class MtsVersionUpdateDelete(RetrieveUpdateDestroyAPIView):
    """
    MTS Version 아이템 수정 삭제하기
    """
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "mts-version-update-delete"

    #--------------------------------------
    #  AUTHORITY
    #--------------------------------------
    permission_classes = [MtsVersionPermission]

    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = MtsVersionSerializer
        return serializer

    def get_queryset(self, **kwargs):
        return MtsVersion.objects.all()

    def put(self, request, *args, **kwargs):
        mts_version = MtsVersion.objects.get(pk=kwargs.get("pk"))
        device = request.data.get("device", None)
        version = request.data.get("version", None)
        comment = request.data.get("comment", None)

        if comment is None:
            return Response(
                data = ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00017.format('comment'))
                , status = status.HTTP_400_BAD_REQUEST
            )

        response = self.update(request, *args, **kwargs)

        user = User.objects.get(id = request.user.get_id())

        body = {
            "user_id"       : request.user.get_id()
            , "emp_no"      : user.emp_no
            , "old_version" : mts_version.version
            , "new_version" : version
            , "device"      : device
            , "comment"     : comment
            , "created_at"  : str(datetime.now())
        }

        log = CentralLogging()
        log.setLog(body, request, UPDATE, response.status_code, 8200)

        # MONGO DB 추가
        logging_utils.set_log(TBL_BCOFFICE_MTS_VERSION_HISTORY, log.toJsonString())

        return response

    def delete(self, request, *args, **kwargs):
        mts_version = MtsVersion.objects.get(pk=kwargs.get("pk"))

        response = self.destroy(request, *args, **kwargs)

        user = User.objects.get(id = request.user.get_id())

        body = {
            "user_id"       : request.user.get_id()
            , "emp_no"      : user.emp_no
            , "old_version" : mts_version.version
            , "new_version" : None
            , "device"      : mts_version.device
            , "comment"     : "버전삭제"
            , "created_at"  : str(datetime.now())
        }

        log = CentralLogging()
        log.setLog(body, request, DELETE, response.status_code, 8200)

        # MONGO DB 추가
        logging_utils.set_log(TBL_BCOFFICE_MTS_VERSION_HISTORY, log.toJsonString())

        return response