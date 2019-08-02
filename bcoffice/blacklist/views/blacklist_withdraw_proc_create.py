from . import *

# 블랙리스트 출금/취소 등록
class BlackListWithdrawProcCreate(CreateAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "blacklist-withdraw-proc-create"

    #--------------------------------------
    #  AUTHORITY
    #--------------------------------------
    permission_classes = [BlackListWithdrawAddrCreatePermission]

    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------


    # 블랙리스트 출금/취소 등록
    def create(self, request, *args, **kwargs):

        mongodb = BCOfficeBlackListMongoDB(collection=TBL_BCOFFICE_BLACKLIST_WITHDRAW_PROC)

        data = {}
        for str in request.data:
            data[str] = request.data[str]

        cur_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user_id  = request.user.get_id()

        withdraw_id = data['withdraw_id']

        if data['type'] == 'done':
            # 출금처리 : 거래소 MQ로 메세지 전송
            mq_utils.request_withdraw(withdraw_id)

        data['user'] = user_id
        data['updated_at'] = cur_date

        history = {'history':
                    {'type': data['type'],
                     'user': user_id,
                    'reason': data['reason'],
                    'created_at': cur_date} }

        mongodb.collection.update({'withdraw_id': withdraw_id},
                                  {'$set': data, '$push': history},
                                  True)
        data['result'] = 'success'
        headers = self.get_success_headers(data)

        data['user'] = User.objects.get(id=data['user']).email
        if '_id' in data.keys():
            del data['_id']
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)