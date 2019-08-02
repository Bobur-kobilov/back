from . import *
from rest_framework.exceptions import *
import math
class UserActivity(APIView):
    name = "user_activity"
    permission_classes = [DailyTotalSalesPermission]
    pagination_class = LimitOffsetPagination

    def get_queryset(self,*args,**kwargs):
        type = kwargs.get('type',None)
        start_date = kwargs.get('start_date',None)
        end_date = kwargs.get('end_date',None)

        if start_date is not None and end_date is not None:
            start_date = start_date + ' 00:00:00'
            end_date = end_date + ' 23:59:59'
        
        if type == 'register':
            queryset = Members.objects.using('exchange') \
            .filter(created_at__range=(start_date,end_date)) \
            .count()
            return queryset
        elif type == 'active':
            queryset = Members.objects.using('exchange') \
            .filter(updated_at__range=(start_date,end_date)) \
            .distinct() \
            .values_list('id', flat=True) \
            .count()
            return queryset
        elif type == 'total':
            queryset = Members.objects.using('exchange') \
            .count()
            return queryset 
        elif type == 'past_user':
            queryset = Members.objects.using('exchange') \
            .filter(created_at__lte=(start_date)) \
            .count()
            return queryset
        elif type == 'present_user':
            queryset = Members.objects.using('exchange') \
            .filter(created_at__lte=(end_date)) \
            .count()
            return queryset
    def get(self,request,*args,**kwargs):
        start_date = request.query_params.get('start_date',None)
        end_date = request.query_params.get('end_date',None)
        
        register_count = self.get_queryset(start_date=start_date,end_date=end_date,type='register')
        active_user = self.get_queryset(start_date=start_date,end_date=end_date,type='active')
        total_users = self.get_queryset(type='total')
        retention_rate = round((active_user/total_users)*100,2)
        past_users = self.get_queryset(type='past_user',start_date=start_date,end_date=end_date)
        present_users = self.get_queryset(type='present_user', start_date=start_date,end_date=end_date)
        growth_rate = ((present_users - past_users)/past_users)*100
        growth_rate = round(growth_rate,2)
        results = [
            {
                "register_count": register_count,
                "active_user": active_user,
                "total_user": total_users,
                "retention_rate":retention_rate,
                "growth_rate": growth_rate
            }
        ]
        return Response(data={"results":results})