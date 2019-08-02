from . import *

class AuthModified(RetrieveUpdateDestroyAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "auth-modified"
    permission_classes = [AuthListCreatePermission]
    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = AuthCreateSerializer
        return serializer

    # 쿼리셋 가져오기
    def get_queryset(self):
        return Auth.objects.all()

    def update(self, request, *args, **kwargs):
        if request.data.get("user_id", None) and request.data.get("roles", None) :
            user_id = int(request.data.get("user_id"))
            roles = request.data.get("roles").split(",")

            is_super_user = False

            user_role_list = list(Auth.objects.values().filter(user_id=user_id))
            exist_role_list = []

            roles.append("ROLE_Default")

            for user_role in user_role_list :
                if user_role['role'] == "ROLE_Super" :
                    roles.append("ROLE_Super")
                    break

            for role in user_role_list:
                result  = False
                for item in roles:
                    if role['role'] == item:
                        result = True
                        break

                if result is False:
                    role_item = Auth.objects.filter(id=role['id'])
                    self.perform_destroy(role_item)
                else :
                    exist_role_list.append(role)

            for item in roles:
                result = False
                for role in exist_role_list:
                    if role['role'] == item:
                        result = True
                        break

                if result is False:
                    data = {}
                    data['user_id'] = user_id
                    data['role'] = item

                    try :
                        auth_serializer = AuthCreateSerializer(data=data)
                        auth_serializer.is_valid(raise_exception=True)
                        auth_serializer.save()
                    except :
                        return Response(auth_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_INF00001), status=status.HTTP_200_OK)
        return Response(data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00015), status=status.HTTP_400_BAD_REQUEST)