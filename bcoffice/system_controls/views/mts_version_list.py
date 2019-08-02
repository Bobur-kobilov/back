from . import *


class MtsVersionList(ListCreateAPIView):
    """
    MTS Version 가져오기
    """
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "mts-version-list"

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

    # 쿼리셋 가져오기
    def get_queryset(self):
        return MtsVersion.objects.all()

    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)

        user = User.objects.get(id = request.user.get_id())

        device = request.data.get("device", None)
        version = request.data.get("version", None)

        body = {
            "user_id"       : request.user.get_id()
            , "emp_no"      : user.emp_no
            , "old_version" : None
            , "new_version": version
            , "device" : device
            , "comment"     : "버전신규 생성"
            , "created_at"  : str(datetime.now())
        }

        log = CentralLogging()
        log.setLog(body, request, CREATE, response.status_code, 8200)

        # MONGO DB 추가
        logging_utils.set_log(TBL_BCOFFICE_MTS_VERSION_HISTORY, log.toJsonString())

        return response