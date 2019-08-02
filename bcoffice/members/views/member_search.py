from . import *
from django.db.models import Q
import re
email_pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"

class MemberSearch(APIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "member-search"
    permission_classes = [MemberPermission]

    def get(self, request, *args, **kwargs):
        keyword = request.query_params.get("keyword", None)

        query_member = Members.objects.using('exchange').values_list('id', flat=True)

        where = []
        if keyword.isnumeric():
            where.append(Q(id=int(keyword)))
            where.append(Q(phone_number=keyword))

        if re.match(email_pattern, keyword):
            where.append(Q(email=keyword))

        if len(where) == 0:
            return Response(
                # "일치하는 값이 없습니다."
                data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00022)
                , status=status.HTTP_404_NOT_FOUND
            )

        query_member = query_member.filter(reduce(operator.__or__, where))
        if query_member.exists():
            member_id = query_member[0]
        else:
            return Response(
                # "일치하는 값이 없습니다."
                data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00022)
                , status=status.HTTP_404_NOT_FOUND
            )

        result = {}
        result['member_id'] = member_id
        return Response(data=result, status=status.HTTP_200_OK)