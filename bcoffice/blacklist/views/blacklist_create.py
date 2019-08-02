from . import *

# 블랙리스트 IP 등록
class BlackListCreate(CreateAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "blacklist-create"

    #--------------------------------------
    #  AUTHORITY
    #--------------------------------------
    permission_classes = [BlackListCreatePermission]

    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------


    # 블랙리스트 IP 등록/해제
    def create(self, request, *args, **kwargs):

        mongodb = BCOfficeBlackListMongoDB(collection=TBL_BCOFFICE_BLACKLIST)

        data = {}
        for str in request.data:
            data[str] = request.data[str]

        cur_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user_id  = request.user.get_id()

        data['user'] = user_id
        data['updated_at'] = cur_date

        history = {'history':
                    {'state': data['state'],
                     'user': user_id,
                    'reason': data['reason'],
                    'created_at': cur_date} }

        mongodb.collection.update({'type': data['type'], 'value': data['value']}, {'$set': data, '$push': history}, True)
        data['result'] = 'success'
        headers = self.get_success_headers(data)

        if '_id' in data.keys():
            del data['_id']
        data['user'] = User.objects.get(id=data['user']).email
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)