from . import *


class HotWithdrawApplyUpdate(UpdateAPIView):
    """
    HOT 출금 실행 업데이트(상태값 변경)
    """
    name = "hot_withdraw_apply_update"
    permission_classes  = [HotWithdrawApplyPermission]

    def get_serializer_class(self):
        serializer = WithdrawApplySerializer
        return serializer

    def get_queryset(self, *args, **kwargs):
        return WithdrawApply.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = {}

        for field in request.data:
            data[field] = request.data[field]

        data['id'] = instance.id
        data['wallet_type'] = instance.wallet_type
        data['currency']    = instance.currency
        data['requester_id'] = instance.requester_id
        data['withdraw_wallet_id'] = instance.withdraw_wallet_id
        data['deposit_wallet_id'] = instance.deposit_wallet_id
        data['withdraw_volume'] = instance.withdraw_volume
        data['reason_id'] = instance.reason_id
        data['etc_reason'] = instance.etc_reason
        data['proc_date'] = datetime.now()
        data['supervisor'] = request.user.get_id()

        withdraw = DepositAddress.objects.get(id=data['withdraw_wallet_id'])
        deposit = DepositAddress.objects.get(id=data['deposit_wallet_id'])

        balance = 0

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

        # 이미 처리된 요청을 다시 처리하는지 확인
        if instance.status > 100 :
            return Response(
                    data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00026)
                    , status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        if int(data['status']) == 200 :
            coinManager = CoinManager()
            coin = 0

            for item in settings.CURRENCY_LIST :
                if data['currency'] == item['id']:
                    coin = item['code'].lower()
                    break

            address = deposit.address
            if deposit.tag is not None:
                address = address + '_' + deposit.tag

            result = coinManager.sendToAddress(
                coin=coin
                , address = address
                , amount = data['withdraw_volume']
            )

            send_result = result.get("result", None)

            if send_result is None:
                """
                CoinManager를 통한 송금이 실패한 경우
                status을 100으로 바꾸고 처리 전 단계로 전환합니다.
                """
                data['status'] = 100
                data['proc_date'] = None
                data['supervisor'] = -1

                serializer = self.get_serializer(instance, data=data, partial=partial)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)

                if getattr(instance, '_prefetched_objects_cache', None):
                    instance._prefetched_objects_cache = {}

                return Response(
                    data=RequestMessage.getMessage(ResponseMessage.MESSAGE_ERR00025)
                    , status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            history = WithdrawHistory(
                currency        = data['currency']
                , deal_type     = 100
                , volume        = data['withdraw_volume']
                , request_date  = instance.created_at
                , approval_date = data['proc_date']
                , txid          = result['result']
            )

            history.withdraw_apply_id = instance.id
            history.supervisor_id = request.user.get_id()
            history.requester_id = data['requester_id']
            history.wallet_id = data['withdraw_wallet_id']

            history.save()

        return Response(serializer.data)