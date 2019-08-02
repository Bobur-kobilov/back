from . import *
from itertools import chain
# 블랙리스트 출금요청 목록조회

class BlackListWithdrawProcList(ListAPIView):
    # --------------------------------------
    #  PROPERTIES
    # --------------------------------------
    name = "blacklist-withdraw-proc-list"
    permission_classes = [BlackListWithdrawAddrListPermission]

    # --------------------------------------
    #  PROPERTIES : FILTER
    # --------------------------------------
    filter_fields = ['id']
    search_fields = []
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    pagination_class = StandardPagination
    page_size_query_param = ""

    def get_serializer_class(self):
        serializer = CoinWithdrawHistorySerializer
        return serializer


    # 쿼리셋 가져오기
    def get_queryset(self, order_id=None, start=None, end=None, member_id=None, aasm_state=None, currency=None, fund_uid=None,withdraw_count=None,same_fund_uid=None,holdType=None,withdraw_address=None):

        query = Withdraws.objects.using("exchange")

        if withdraw_count == 'total' and member_id is not None:
            query = query.filter(member_id=int(member_id)) \
            .filter(aasm_state="done") \
            .count()
            print(query)
            return query
        if withdraw_count == 'same_fund_uid' and member_id is not None:
            query = query.filter(member_id=int(member_id)) \
            .filter(aasm_state="done") \
            .filter(fund_uid=same_fund_uid) \
            .count()
            return query
        # 주문번호 검색
        if order_id is not None and order_id is not '':
            query = query.filter(id=order_id)

        # 회원검색
        if member_id is not None:
            query = query.filter(member_id=int(member_id))

        # 출금주소
        if fund_uid is not None:
            query = query.filter(fund_uid=fund_uid)

        # 조회시간 설정
        if start is not None and start is not '' and str(start) != 'Invalid date':
            start_date = start + ' 00:00:00'
            query = query.filter(created_at__gte=start_date)
        if end is not None and end is not '' and str(end) != 'Invalid date':
            end_date = end + ' 23:59:59'
            query = query.filter(created_at__lte=end_date)

        # 거래상태 조회
        if aasm_state == 'wait_admin_confirm':
            query = query.filter(aasm_state=aasm_state)
        elif aasm_state == 'failed':
            minute_ago = datetime.today() - timedelta(minutes=1)
            query = query.filter(aasm_state=aasm_state)

        # 암호화폐 조회
        if currency is not None and currency is not '' and currency != 'all':
            currency = currency.split(',')
            query = query.filter(currency__in=currency)

        if holdType is not None and holdType is not '':
            query = query.filter(type=holdType).filter(aasm_state="wait_admin_confirm")

        if withdraw_address is not None and withdraw_address is not '':
            query = query.filter(fund_uid = withdraw_address)
        return query

    def get_deposit_query(self,memberID=None):
        query = Deposits.objects.using('exchange') \
        .filter(member_id=int(memberID)) \
        .count()
        return query

    def get_balance_query(self,member_id=None,coin=None):
        query = Accounts.objects.using('exchange').values('balance') \
        .filter(member_id=int(member_id)) \
        .filter(currency=coin)
        return query
    
    def checkAddress(self,wallet_address=None):
        if wallet_address is not None:
            query = PaymentAddresses.objects.using("exchange")
            query = query.filter(address=wallet_address).count()
            if query > 0:
                response = True
            else:
                response = False
            return response

    def get(self, request, *args, **kwargs):

        # 페이지네이션
        limit  = request.query_params.get('limit', None)
        offset = request.query_params.get('offset', None)

        # 회원정보로 검색
        member_id = request.query_params.get('member_id', None)

        currency = request.query_params.get('currency', None)
        address = request.query_params.get('address', None)

        withdraw_address = request.query_params.get('withdraw_address', None)


        #  wait : 출금대기, cancel : 출금취소, done : 출금완료
        type = request.query_params.get('type', None)
        holdType = None
        aasm_state = None
        if type is not None:
            if type == 'wait':
                aasm_state = 'wait_admin_confirm'
            elif type == 'failed':
                aasm_state = type
            elif type == 'Hold':
                holdType = type

        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)

        queryset = self.get_queryset(
              start=start_date
            , end=end_date
            , member_id=member_id
            , aasm_state=aasm_state
            , currency=currency
            , fund_uid=address
            , holdType = holdType
            , withdraw_address = withdraw_address
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

        mongodb = BCOfficeBlackListMongoDB(collection=TBL_BCOFFICE_BLACKLIST_WITHDRAW_PROC)

        # blacklist 여부를 추가
        params = {}
        for obj in serializer.data:
            params['withdraw_id'] = obj['id']
            obj['isBlackList'] = mongodb.collection.find(params).count()

        userData = serializer.data
        for i in range ( len(userData)):
            deposit_count = self.get_deposit_query(userData[i]['member_id'])
            withdraw_count = self.get_queryset(member_id=userData[i]['member_id'],withdraw_count='total')
            same_fund_uid_count = self.get_queryset(member_id=userData[i]['member_id'],same_fund_uid=userData[i]['fund_uid'],withdraw_count="same_fund_uid")
            wallet_address_local = self.checkAddress(wallet_address=userData[i]['fund_uid'])
            balance = self.get_balance_query(member_id=userData[i]['member_id'],coin=userData[i]['currency'])
            balance = list(balance)
            left_balance = float(balance[0]['balance']) - float(userData[i]['amount'])
            serializer.data[i]['same_fund_uid_count'] = same_fund_uid_count
            serializer.data[i]['deposit_count'] = deposit_count
            serializer.data[i]['withdraw_count'] = withdraw_count
            serializer.data[i]['left_balance'] = left_balance
            serializer.data[i]['wallet_address_local'] = wallet_address_local
        return self.get_paginated_response(serializer.data)

