from . import *


# 거래소 회원 잔고조회
class MemberBalanceList(ListAPIView):
    #--------------------------------------
    #  VARIABLES
    #--------------------------------------
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "member-balance-list"
    permission_classes = [MemberBalancePermission]
    #--------------------------------------
    #  PROPERTIES : FILTER
    #--------------------------------------
    ordering_fields     = ['currency']
    ordering            = ['currency']
    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = MemberBalanceSerializer
        return serializer
    
    # 쿼리셋 가져오기
    def get_queryset(self, member_id = None):
        query = Accounts.objects.using("exchange").filter(member_id = member_id)
        return query

    def list(self, request, *args, **kwargs):
        member_id = request.query_params.get("member_id", None)

        if member_id is None :
            return Response (
                # "회원검색 값을 넣어주세요."
                data    = ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00007)
                ,status = status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.get_queryset(member_id = member_id)

        if queryset is None:
            return Response (
                    # "일치하는 값이 없습니다."
                    data    = ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00008)
                    ,status = status.HTTP_404_NOT_FOUND
                )
            
        queryset = self.filter_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        
        balance_list = serializer.data
        
        for item in balance_list:
            address = PaymentAddresses.objects.using("exchange").filter(account_id=item['id'])
            if address.exists():
                item['payment_address'] = address[0].address
            else :
                item['payment_address'] = ""
            item['balance']         = float(item['balance'])
            item['locked']          = float(item['locked'])
            item['total_coin']      = float(item['balance']) + float(item['locked'])
            item['exchange_coin']   = float(item['total_coin'])
            item['exchange_usd']    = ValuationAssetsUtil.get_valuation_for_dollar(int(item['currency']), item['total_coin'])

        return Response(data=balance_list)