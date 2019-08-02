
from . import *
from datetime import datetime
from dateutil.relativedelta import relativedelta
# 거래소 회원 목록
class MemberList(ListAPIView):
    # --------------------------------------
    #  PROPERTIES
    # --------------------------------------
    name = "member-list"
    permission_classes = [MemberPermission]
    # --------------------------------------
    #  PROPERTIES : FILTER
    # --------------------------------------
    filter_fields = []
    search_fields = ['phone_number', 'email', 'display_name', 'id']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    pagination_class = StandardPagination
    page_size_query_param = ""

    # --------------------------------------
    #  OVERRIDEN METHODS
    # --------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = MemberSerializer
        return serializer

    # 쿼리셋 가져오기
    def get_queryset(self, start=None, end=None, *args, **kwargs):
        query = Members.objects.using("exchange")

        # security_level    = kwargs['security_level']
        state = kwargs['state']
        txid = kwargs['txid']
        inactivePeriod = kwargs['inactivePeriod']
        member_id = kwargs['member_id']
        # if security_level is not None :
        #     if security_level == '1' :
        #         query = (
        #             query
        #             .filter(email_allowed = 1)
        #             .filter(Q(sms_allowed = 0)|Q(sms_allowed = None))
        #             .filter(Q(kyc_activated = 0)|Q(kyc_activated = None))
        #         )
        #     elif security_level == '2' :
        #         query = (
        #             query
        #             .filter(email_allowed = 1)
        #             .filter(sms_allowed = 1)
        #             .filter(Q(kyc_activated = 0)|Q(kyc_activated = None))
        #         )
        #     elif security_level == '3' :
        #         query = (
        #             query
        #             .filter(email_allowed = 1)
        #             .filter(sms_allowed = 1)
        #             .filter(kyc_activated = 1)
        #         )

        where = []
        state_dic = ['restricted', 'disabled', 'deleted']
        if state in state_dic:
            if state == 'restricted':
                where.append(Q(restricted=1))
            elif state == 'disabled':
                where.append(Q(disabled=1))
            elif state == 'deleted':
                where.append(Q(deleted=1))

        if where.__len__() > 0:
            query = query.filter(reduce(operator.__or__, where))

        # 가입일시 설정
        if start is not None and start is not '':
            start_date = start + ' 00:00:00'
            query = query.filter(created_at__gte=start_date)

        if end is not None and end is not '':
            end_date = end + ' 23:59:59'
            query = query.filter(created_at__lte=end_date)

        if txid and txid is not '':
            txid_member_list = []
            deposit_member_list = list(Deposits.objects.using('exchange').values_list('member_id', flat=True).filter(txid=txid))
            withdraw_member_list = list(Withdraws.objects.using('exchange').values_list('member_id', flat=True).filter(txid=txid))
            txid_member_list.extend(deposit_member_list)
            txid_member_list.extend(withdraw_member_list)
            # 중복제거
            txid_member_list = list(set(txid_member_list))
            query = query.filter(id__in = txid_member_list)

        if inactivePeriod is not None and inactivePeriod is not '':
            today = datetime.today()
            current_month = datetime(today.year,today.month,1)
            inactivePeriod = current_month - relativedelta(months=int(inactivePeriod))
            query = query.filter(updated_at__lte=inactivePeriod)    
        
        if member_id is not None and member_id is not '':
            query = query.filter(id=member_id)

        return query

    def get_accountId(self, wallet_address):
        print(wallet_address)
        query = PaymentAddresses.objects.using('exchange').values('account_id') \
        .filter(address=wallet_address)
        print(query)
        if(len(query)>0):
            return query[0]['account_id']

    def get_memberId(self, account_id):
        print(account_id)
        query = Accounts.objects.using('exchange').values('member_id') \
        .filter(id=account_id)
        if (len(query)>0):
            return query[0]['member_id']


    def list(self, request, *args, **kwargs):
        inactivePeriod = request.query_params.get('inactive',None)
        # 가입일시 선택
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        # security_level  = request.query_params.get('security_level' , None)
        activated = request.query_params.get('activated', None)
        state = request.query_params.get('state', None)
        txid = request.query_params.get('txid', None)
        wallet_address = request.query_params.get('wallet_address',None)
        member_id = ''
        if wallet_address is not None and wallet_address is not '':
            account_id = self.get_accountId(wallet_address)
            member_id = self.get_memberId(account_id)
        queryset = self.get_queryset(
            start=start_date
            , end=end_date
            # , security_level    = security_level
            , activated=activated
            , state=state
            , txid=txid
            , inactivePeriod = inactivePeriod
            , member_id = member_id
        )

        if queryset is None:
            return Response(
                # "일치하는 값이 없습니다."
                data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00008)
                , status=status.HTTP_404_NOT_FOUND
            )

        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)

        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

