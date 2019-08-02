from rest_framework import serializers
# from rest_framework_mongoengine.serializers import DocumentSerializer
# base.txt에 추가 (django-rest-framework-mongoengine)
from becoin.model   import ( 
    Members
    , Accounts
    , SignupHistories
    , AccountVersions
    , ReferralFeeHistories
    , TwoFactors
)
from .models        import ReferralList


class TwoFactorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwoFactors
        fields = [
            'id'
            , 'member_id'
            , 'otp_secret'
            , 'last_verify_at'
            , 'activated'
            , 'type'
            , 'refreshed_at'
        ]

# 거래소 사용자 목록
class MemberSerializer(serializers.ModelSerializer):
    two_factors = TwoFactorsSerializer(many=True, read_only=True)
    class Meta:
        model = Members
        fields = [
            'id'
            , 'sn'
            , 'display_name'
            , 'email'
            , 'identity_id'
            , 'created_at'
            , 'updated_at'
            , 'state'
            , 'activated'
            , 'country_code'
            , 'phone_number'
            , 'disabled'
            , 'api_disabled'
            , 'nickname'
            , 'email_allowed'
            , 'sms_allowed'
            , 'kyc_activated'
            , 'restricted'
            , 'deleted'
            , 'two_factors'
        ]


# 거래소 사용자 정보 수정
class MemberUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = [
            'id'
            , 'display_name'
            , 'nickname'
        ]


# 거래소 사용자 잔고
class MemberBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = [
            'id'
            , 'member_id'
            , 'currency'
            , 'balance'
            , 'locked'
            , 'created_at'
            , 'updated_at'
            , 'in_field'
            , 'out'
            , 'default_withdraw_fund_source_id'
            , 'avg_price'
            , 'total_amount'
        ]


# 거래소 회원 자산변동이력
class MemberAccountHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountVersions
        fields = [
            'id'
            , 'member_id'
            , 'account_id'
            , 'reason'
            , 'balance'
            , 'locked'
            , 'fee'
            , 'amount'
            , 'modifiable_id'
            , 'modifiable_type'
            , 'created_at'
            , 'updated_at'
            , 'currency'
            , 'fun'
            , 'avg_price'
            , 'total_amount'
        ]


# 로그인 이력 시리얼라이저
class LogInSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignupHistories
        fields = [
            'id'
            , 'member_id'
            , 'ip'
            , 'accept_language'
            , 'ua'
            , 'created_at'
        ]


# 회원 정정이력 시리얼라이저
# class MemberModifySerializer(DocumentSerializer):
#     class Meta:
#         model = BcofficeMemberModifies
#         fields = [
#             'user_id'
#             ,'member_id'
#             ,'mod_fileds'
#             ,'memo'
#             ,'created_at'
#             ,'origin_data'
#             ,'mod_data'
#         ]


# 추천인정보 피추천인 시리얼라이저
class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralList
        fields = [
            'id'
            , 'referral_id'
            , 'member_id'
            , 'created_at'
            , 'email'
            , 'phone'
        ]


# 추천인정보 지급내역 시리얼라이저
class ReferralPaySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralFeeHistories
        fields = [
            'id'
            , 'trade_id'
            , 'currency'
            , 'amount'
            , 'fee'
            , 'member_id'
            , 'created_at'
        ]