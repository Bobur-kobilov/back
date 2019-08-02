from rest_framework import serializers
from becoin.model import Accounts, Deposits, Withdraws

class BankBalanceSerializer(serializers.Serializer):
    currency        = serializers.IntegerField()
    balance_total   = serializers.FloatField()
    locked_total    = serializers.FloatField()

class BankDepositHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposits
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
        ]

class BankWithdrawHistorySerializer(serializers.ModelSerializer):
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