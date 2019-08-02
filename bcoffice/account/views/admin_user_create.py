from . import *
from bcoffice.migrate_init_value import Account

class AdminUserCreate(APIView):
    name = "admin-user-create"

    def get_serializer_class(self):
        serializer = UserCreateSerializer
        return serializer

    def post(self, request, *args, **kwargs):
        superuser = User.objects.filter(email = 'administrator@domain.com')

        # 존재하지 않으면 생성
        if superuser.exists() is False:
            data = {}
            data['email'] = Account.DEFAULT_SUPER_USER['EMAIL']
            data['password'] = Account.DEFAULT_SUPER_USER['PASSWORD']
            data['cell_phone'] = "010-0000-0000"
            data['name'] = "administrator"
            data['eng_name'] = "administrator"
            data['active'] = True
            data['status'] = STATUS['ACTV']
            data['joined_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data['close_date'] = None
            data['dept_type'] = 1
            data['dept_rank'] = 1
            data['dept_duty'] = 1

            serializer = UserCreateSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            user = User.objects.get(email = data['email'])
            auth = Auth.objects.get(user_id = user.id)
            s_auth = Auth(user_id = user.id, role = 'ROLE_Super')
            s_auth.save()

        return Response(status=status.HTTP_200_OK)