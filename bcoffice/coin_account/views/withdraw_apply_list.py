from . import *

class WithdrawApplyList(ListCreateAPIView):
    name = "hot_withdraw_apply"
    permission_classes  = [WithdrawApplyPermission]
    pagination_class    = LimitOffsetPagination

    def get_serializer_class(self):
        serializer = WithdrawApplySerializer
        return serializer

    def get_queryset(self, *args, **kwargs):
        queryset = WithdrawApply.objects.all()

        requester   = kwargs.get('requester', None)
        start_date  = kwargs.get('start_date', None)
        end_date    = kwargs.get('end_date', None)
        currency    = kwargs.get('currency', None)
        wallet_type    = kwargs.get('wallet_type', None)
        status    = kwargs.get('status', None)

        if requester is not None :
            queryset = queryset.filter(requester__emp_no = requester)

        if start_date is not None :
            start_date += " 00:00:00"
            queryset = queryset.filter(created_at__gte = start_date)

        if end_date is not None :
            end_date += " 23:59:59"
            queryset = queryset.filter(created_at__lte = end_date)

        if currency is not None :
            queryset = queryset.filter(currency = currency)

        if wallet_type is not None :
            queryset = queryset.filter(wallet_type = wallet_type)

        if status is not None :
            queryset = queryset.filter(status = status)

        return queryset.order_by("-created_at")

    def list(self, request, *args, **kwargs):
        requester   = request.query_params.get('requester', None)
        start_date  = request.query_params.get('start_date', None)
        end_date    = request.query_params.get('end_date', None)
        currency    = request.query_params.get('currency', None)
        wallet_type = request.query_params.get('wallet_type', None)
        status      = request.query_params.get('status', None)

        if wallet_type is None :
            return Response(
                data = ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00017.format("wallet_type"))
                , status=status.HTTP_400_BAD_REQUEST
            )

        queryset = self.get_queryset(
            requester       = requester
            , start_date    = start_date
            , end_date      = end_date
            , currency      = currency
            , wallet_type   = wallet_type
            , status        = status
        )

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)

            #print(serializer.data)

            for item in serializer.data :
                item['supervisor_info'] = None

                if item['supervisor'] > 0 :
                    user = User.objects.all().get(id = item['supervisor'])
                    item['supervisor_info'] = UserAuthSerializer(user, many=False).data

            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = {}

        for field in request.data:
            data[field] = request.data[field]

        withdraw = DepositAddress.objects.get(id=data['withdraw_wallet'])
        balance = 0

        getBalanceCoinManager = False
        getBalanceOutsideList = ['BTC', 'QTUM', 'BCH', 'ADA']

        if data['wallet_type'] == 'COLD':
            for item in settings.CURRENCY_LIST:
                if int(data['currency']) == int(data['currency']):
                    currency = item['code'].upper()
                    break
            if currency in getBalanceOutsideList:
                balance = CoinUtil.getCoinBalance(data['currency'], withdraw.address)
            else:
                getBalanceCoinManager = True

        elif data['wallet_type'] == 'HOT' or getBalanceCoinManager == True:
            manager = CoinManager()
            coin_name = manager.transCurrencyIdToName(data['currency'])

            if coin_name is None:
                return Response(
                        data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00030)
                        , status=status.HTTP_400_BAD_REQUEST)

            balance = float( manager.getCoinBalance(coin_name)['result'] )


        # 지갑잔고보다 요청수량이 더 많은지 확인
        if data['withdraw_volume'] > balance :
            return Response(
                    data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00027)
                    , status=status.HTTP_400_BAD_REQUEST)

        withdrawApply = WithdrawApply(
            wallet_type = data['wallet_type']
            , currency = data['currency']
            , etc_reason = data.get('etc_reason', None)
            , withdraw_volume = data.get('withdraw_volume', None)
        )

        withdrawApply.requester_id = request.user.get_id()
        withdrawApply.withdraw_wallet_id = data['withdraw_wallet']
        withdrawApply.deposit_wallet_id = data['deposit_wallet']
        withdrawApply.reason_id = data['reason']

        withdrawApply.save()


        return Response(data={}, status=status.HTTP_201_CREATED)