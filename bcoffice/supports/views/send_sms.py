from . import *


# SMS 발송
class SendSMSView(APIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "send_sms"
    permission_classes = [SendPermission]

    # SMS 발송 내역 가져오기
    def get(self, request, *args, **kwargs):
        limit = request.query_params.get("limit", None)
        offset = request.query_params.get("offset", None)
        data = {}

        mongodb = BCOfficeHistoryMongoDB(collection=TBL_BCOFFICE_SEND_SMS_HISTORY)
        result = (mongodb.collection.find().sort('_id', pymongo.DESCENDING))
        count = mongodb.collection.find().count()

        if limit is not None and offset is not None:
            result = result[int(offset):int(offset) + int(limit)]
            data['count'] = count


        data['results'] = []

        for item in result :
            obj = {}
            obj['header'] = item['header']
            obj['body'] = item['body']

            sqlTime = obj['header']['sqlTime']
            created_at = obj['body']['created_at']

            if isinstance( sqlTime, str ):
                sqlTime = datetime.strptime(sqlTime, '%Y-%m-%d %H:%M:%S.%f')

            if isinstance( created_at, str ):
                created_at = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S.%f')

            sqlTime = sqlTime.strftime("%Y-%m-%d %H:%M:%S")
            created_at = created_at.strftime("%Y-%m-%d %H:%M:%S")

            obj['header']['sqlTime'] = sqlTime #date_util.utc_datetime_to_local(obj['header']['sqlTime'])
            obj['body']['created_at'] = created_at #date_util.utc_datetime_to_local(obj['body']['created_at'])

            data['results'].append(obj)

        mongodb.close()

        return Response(data = data, status = status.HTTP_200_OK)

    # SMS 발송하기 및 Log남기기
    def post(self, request, *args, **kwargs):
        targets = request.data.get('targets', None)
        message     = request.data.get('message', None)
        send_type = request.data.get('send_type', None)

        target_list = []
        user_id     = request.user.get_id()

        if message is None :
            return Response(
                data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00017.format("메시지"))
                , status=status.HTTP_400_BAD_REQUEST)

        if send_type is not None and send_type == 'all':
            target_list = list(Members.objects.using('exchange').filter(disabled=0).exclude(phone_number__isnull=True).exclude(phone_number__exact='').values_list('phone_number', flat=True))
        else :
            target_list = targets.split(',')

        SendSMS.send(
            sender_id       = user_id
            , target_list   = target_list
            , message       = message
        )

        user = User.objects.get(id = user_id)

        body = {
            "user_id"       : user_id
            , "emp_no"      : user.emp_no
            , "target_count": target_list.__len__()
            , "target_list" : target_list
            , "message"     : message
            , "created_at"  : str(datetime.now())
        }

        response = Response(data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_INF00001), status=status.HTTP_200_OK)

        log = CentralLogging()
        log.setLog(body, request, CREATE, response.status_code, 5200)

        # MONGO DB 추가
        logging_utils.set_log(TBL_BCOFFICE_SEND_SMS_HISTORY, log.toJsonString())

        return response