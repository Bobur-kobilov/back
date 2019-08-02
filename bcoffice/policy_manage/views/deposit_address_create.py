from . import *


class DepositAddressCreate(CreateAPIView):
    """
    입금주소 작성하기
    """
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "deposit-address-list"
    permission_classes = [DepositAddressCreatePermission]
    serializer_class = DepositAddressCreateSerializer

    #--------------------------------------
    #  METHODS
    #--------------------------------------
    def create(self, request, *args, **kwargs):
        data = data = {}

        for item in request.data:
            data[item] = request.data[item]

        data['author'] = request.user.get_id()
        currency_item = ValuationAssetsUtil.get_currency_item(int(data['currency']))

        if not "address_type" in data:
            return Response(
                    data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00017.format('address_type'))
                    , status=status.HTTP_400_BAD_REQUEST
                )

        if currency_item is None:
            return Response(
                    data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00021)
                    , status=status.HTTP_400_BAD_REQUEST
                )

        if data['address_type'] == constants.ADDRESS_TYPE_INSIDE:
            try :
                last_deposit_item = DepositAddress.objects.filter(currency=currency_item['id'], address_type=data['address_type'], wallet_type=data['wallet_type']).order_by('-id')[0]                
            except :
                last_deposit_item = None

            if last_deposit_item is not None and last_deposit_item.nick is not None:
                last_deposit_nick = last_deposit_item.nick
                code_count = last_deposit_nick.split('-')[1]
                count = int(code_count[1:code_count.__len__()])
            else :
                count = 0

            wallet_type = ""

            # address_type이 INSIDE인 경우 wallet_type은 필수 값이 된다.
            if not "wallet_type" in data:
                return Response(
                    data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00017.format('wallet_type'))
                    , status=status.HTTP_400_BAD_REQUEST
                )

            if data['wallet_type'] == constants.WALLET_TYPE_HOT :
                wallet_type = 'H'
            elif data['wallet_type'] == constants.WALLET_TYPE_COLD :
                wallet_type = 'C'

            data['nick'] = currency_item['code'].upper() + "-" + wallet_type + '{0:04d}'.format(count + 1)

        # TODO: 제거
        if currency_item['code'] in settings.TAG_COINS:
            if data['tag'] is None or data['tag'] == '' :
                return Response(
                    data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00017.format('tag'))
                    , status=status.HTTP_400_BAD_REQUEST
                )

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)