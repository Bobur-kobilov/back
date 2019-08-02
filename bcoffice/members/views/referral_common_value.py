from . import *


# 추천인정보 상단 값 (추천코드 / 추천인ID / 피추천인 / 총 지급수량 / 커미션 비율 )
class ReferralCommonValue(APIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "referral-common-value"
    permission_classes = [ReferralCommonValuePermission]

    def get(self, request, *args, **kwargs):
        member_id = request.query_params.get("member_id", None)

        if member_id is None:
            return Response(
                data = ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00017.format("member_id"))
                , status = status.HTTP_400_BAD_REQUEST
            )

        referral_code = ""
        referral_id = ""
        referral_fee = 0
        referral_fee_personal = 0
        referral_count = 0
        referral_amount = 0

        try :
            referral = Referrals.objects.using('exchange').get(member_id = member_id)
            referral_code = referral.referral_id
            referral_fee = referral.fee
            referral_count  = self.referral_count(referral_code)
            referral_amount = self.referral_amount(referral_code)
        except: # 추천코드를 생성하지 않은 사용자는 exception이 발생함
            pass

        referral_infos = ReferralInfos.objects.using('exchange').values('fee').get(pk = 1)

        # 수수료율은 개인별 수수료율과 설정 수수료율이 있는데
        # 개인 수수료율을 노출할 때는 두가지 중 높은 쪽을 보여준다.
        if referral_fee is None :
            referral_fee = 0
            referral_fee_personal = 0
            referral_fee = float( referral_infos['fee'] )
        else :
            referral_fee = float(referral_fee)
            referral_fee_personal = float(referral_fee)
            referral_fee = referral_fee + float(referral_infos['fee'])

        referral_id     = self.referral_id(member_id)
        
        return Response({
            'referral_code': referral_code #추천코드
            , 'referral_id': referral_id # 추천인 ID
            , 'referral_count': referral_count # 피추천인 수
            , 'referral_amount': referral_amount # 총 수수료 지급수량
            , 'referral_fee': referral_fee # 적용 커미션
            , 'referral_fee_common' : float(referral_infos['fee']) # 공통 커미션
            , 'referral_fee_personal' : referral_fee_personal # 개별 커미션
        })

    # 추천인ID
    def referral_id(self, member_id = None):
        try :
            query = ReferralFriends.objects.using('exchange').values('referral_id').get(member_id = member_id)
            referral_id = query['referral_id']
            referrals = Referrals.objects.using('exchange').values('member_id').get(referral_id = referral_id)
            referral_id = referrals['member_id']
        except : # 추천인 ID 값이 없는 경우 dose not exist 오류가 발생한다.
            referral_id = ""

        return referral_id

    # 추천인수
    def referral_count(self, referral_code = None):
        referral_count = (
            ReferralFriends.objects.using('exchange')
            .filter(referral_id=referral_code)
            .aggregate(count=Count('referral_id'))
        )

        return referral_count["count"]

    # 총 지급수량
    def referral_amount(self, referral_code = None):
        query = ReferralFeeHistories.objects.using('exchange').values('amount', 'currency').filter(referral_id = referral_code)
        referral_amount = 0

        for obj in query:
            referral_amount += ValuationAssetsUtil.coin_exchange(
                obj['currency']
                , ValuationAssetsUtil.get_currency_item_for_code('btc')['id']
                , float( obj['amount'] )
            )

        return referral_amount