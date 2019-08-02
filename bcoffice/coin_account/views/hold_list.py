from . import *
from rest_framework.exceptions import *
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

class HoldList(APIView):
  name = "hold-list"
  permission_classes = [permissions.IsAuthenticated]
  def post_query(self, *args, **kwargs): 
    member_id = kwargs.get('member_id',None)

  def put(self,request, *args, **kwargs):

    member_id = request.data.get('member_id',None)
    withdraw_id = request.data.get('withdraw_id',None)

    #Modify type to 'Hold'
    withdraw = Withdraws.objects.using('exchange').get(member_id=member_id,id=withdraw_id)
    if (withdraw.type == 'Hold'):
      withdraw.type = ''
    else:
      withdraw.type = 'Hold'

    withdraw.save()

    return Response({'success': 'success'}, status=200)
    
