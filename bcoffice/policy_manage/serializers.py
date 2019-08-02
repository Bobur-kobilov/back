from rest_framework import serializers
from account.serializers import (
    UserAuthSerializer
)
from .models import (
    SystemAlarm
    , DepositAddress
    , WalletRule
)

class SystemAlarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemAlarm
        fields = [
            'id'
            , 'alarm_code'
            , 'is_sms'
            , 'is_email'
        ]

class DepositAddressSerializer(serializers.ModelSerializer):
    author = UserAuthSerializer()

    class Meta:
        model = DepositAddress
        fields = [
            'id'
            , 'author'
            , 'currency'
            , 'address_type'
            , 'wallet_type'
            , 'address'
            , 'nick'
            , 'tag'
            , 'created_at'
            , 'updated_at'
        ]

class DepositAddressCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositAddress
        fields = [
            'id'
            , 'author'
            , 'currency'
            , 'address_type'
            , 'wallet_type'
            , 'address'
            , 'nick'
            , 'tag'
            , 'created_at'
            , 'updated_at'
        ]

class WalletRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletRule
        fields = [
            'id'
            , 'currency'
            , 'target_rate'
        ]