from . import *

#------------------------------------------------------------------------------
#
#    LOGIN / LOGOUT
#
#------------------------------------------------------------------------------
#사용자 로그아웃
@api_view(['POST'])
def user_logout(request):
    if request.user :
        user = request.user
        User.objects.filter(email=user).update(secret=uuid.uuid4())
        auth.logout(request)
    return Response(status=status.HTTP_200_OK)