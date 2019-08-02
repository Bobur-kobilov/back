from rest_framework import serializers
from becoin.model   import Accounts, Withdraws
from .models        import DepositsAdd, WithdrawApply, WithdrawReason, WithdrawHistory

from account.serializers import UserAuthSerializer
from policy_manage.serializers import DepositAddressSerializer

# 암호화폐 잔고 조회
class CoinBalanceSerializer(serializers.Serializer):
    currency        = serializers.IntegerField()
    balance_total   = serializers.FloatField()
    locked_total    = serializers.FloatField()


# 암호화폐 입금내역 조회
class CoinDepositHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositsAdd
        fields =[
            'id'
            , 'account_id'
            , 'member_id'
            , 'currency'
            , 'amount'
            , 'fee'
            , 'fund_uid'
            , 'fund_extra'
            , 'txid'
            , 'state'
            , 'aasm_state'
            , 'created_at'
            , 'updated_at'
            , 'done_at'
            , 'confirmations'
            , 'type'
            , 'payment_transaction_id'
            , 'txout'
            , 'address'
        ]


# 암호화폐 출금내역 조회
class CoinWithdrawHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdraws
        fields =[
            'id'
            , 'sn'
            , 'account_id'
            , 'member_id'
            , 'currency'
            , 'amount'
            , 'fee'
            , 'fund_uid'
            , 'fund_extra'
            , 'created_at'
            , 'updated_at'
            , 'done_at'
            , 'txid'
            , 'aasm_state'
            , 'sum'
            , 'type'
        ]

class WithdrawReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithdrawReason
        fields =[
            'id'
            , 'code'
            , 'description'
            , 'reason_type'
        ]

class WithdrawApplySerializer(serializers.ModelSerializer):
    requester = UserAuthSerializer(many=False, read_only=True)
    # supervisor = UserSerializer(many=False, read_only=True)
    withdraw_wallet = DepositAddressSerializer(many=False, read_only=True)
    deposit_wallet = DepositAddressSerializer(many=False, read_only=True)
    reason = WithdrawReasonSerializer(many=False, read_only=True)

    class Meta:
        model = WithdrawApply
        fields = [
            'id'
            , 'wallet_type'
            , 'currency'
            , 'requester'
            , 'supervisor'
            , 'withdraw_wallet'
            , 'deposit_wallet'
            , 'withdraw_volume'
            , 'reason'
            , 'etc_reason'
            , 'created_at'
            , 'updated_at'
            , 'proc_date'
            , 'status'
        ]

class WithdrawHistorySerializer(serializers.ModelSerializer):
    supervisor = UserAuthSerializer(many=False, read_only=True)
    requester = UserAuthSerializer(many=False, read_only=True)
    withdraw_apply = WithdrawApplySerializer(many=False, read_only=True)
    wallet = DepositAddressSerializer(many=False, read_only=True)
    
    class Meta:
        model = WithdrawHistory
        fields = [
            'id'
            , 'withdraw_apply'
            , 'supervisor'
            , 'requester'
            , 'currency'
            , 'deal_type'
            , 'volume'
            , 'wallet'
            , 'request_date'
            , 'approval_date'
            , 'created_at'
            , 'txid'
        ]

# 현재 사용하지 않음, 추후 Excel Renderer 사용시 사용
class DailyTotalSalesSerializer(serializers.ModelSerializer):    
    currency = serializers.CharField()
    volume = serializers.DecimalField(max_digits=32, decimal_places=16)
    usd_volume = serializers.DecimalField(max_digits=32, decimal_places=16)
    fee = serializers.DecimalField(max_digits=32, decimal_places=16)
    usd_fee = serializers.DecimalField(max_digits=32, decimal_places=16)
    except_fee = serializers.DecimalField(max_digits=32, decimal_places=16)
    except_usd_fee = serializers.DecimalField(max_digits=32, decimal_places=16)
    net = serializers.DecimalField(max_digits=32, decimal_places=16)
    usd_net = serializers.DecimalField(max_digits=32, decimal_places=16)