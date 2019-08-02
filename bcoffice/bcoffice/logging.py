import datetime
import json

CREATE = "create"
READ = "read"
UPDATE = "update"
DELETE = "delete"

class LogHeader:
    # 접근 IP 번호
    ip = ""
    # user-agent
    userAgent = ""
    # referer 정보
    referer = ""
    # data 수정 or 조회 시간
    sqlTime = str(datetime.datetime.now())
    # 변경시스템(거래소, Backoffice)
    system = "BackOffice"
    # 사용자 ID(PK number)
    userId = -1
    # 화면번호
    screenNo = -1
    # 수행한 명령(Create: 생성, Read: 조회, Update: 수정, Delete: 삭제)
    action = ""
    # API URL
    apiURL = ""

    # 응답코드(200, 201, 400, 500 등)
    status = -1

class LogModel:
    header = LogHeader()
    body = {}

class CentralLogging:
    def __init__(self):
        self.log = LogModel()

    def setLog(self, body, request, action = None, status = None, screen_no = -1):
        self.log.header.ip          = request.META['REMOTE_ADDR']
        self.log.header.userAgent   = request.META['HTTP_USER_AGENT']
        self.log.header.userId      = request.user.id
        self.log.header.apiURL      = request.META['PATH_INFO']
        self.log.header.status      = status
        self.log.header.screenNo    = screen_no

        if request.META.get('HTTP_REFERER', False) :
            self.log.header.referer = request.META['HTTP_REFERER']
        else :
            self.log.header.referer = ""

        if action is None :
            if request.META['REQUEST_METHOD'] == 'GET' :
                self.log.header.action = READ
            elif request.META['REQUEST_METHOD'] == 'POST' :
                self.log.header.action = CREATE
            elif request.META['REQUEST_METHOD'] == 'PUT' or request.META['REQUEST_METHOD'] == 'PATCH' :
                self.log.header.action = UPDATE
            elif request.META['REQUEST_METHOD'] == 'DELETE' :
                self.log.header.action = DELETE
            else :
                self.log.header.action = 'undefined'
        else :
            self.log.header.action = action

        self.log.body = body

        return self

    def toDictionary(self):
        dic = {}

        dic['header'] = {
            'ip': self.log.header.ip,
            'userAgent': self.log.header.userAgent,
            'referer': self.log.header.referer,
            'sqlTime': self.log.header.sqlTime,
            'system': self.log.header.system,
            'userId': self.log.header.userId,
            'screenNo': self.log.header.screenNo,
            'action': self.log.header.action,
            'apiURL': self.log.header.apiURL
        }

        dic['body'] = self.log.body

        return dic

    def toJson(self):
        result = self.toDictionary()
        return json.dump(result)

    def toJsonString(self):
        result = self.toDictionary()
        return json.dumps(result)
