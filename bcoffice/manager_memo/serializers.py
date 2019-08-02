from rest_framework import serializers

from account.serializers import UserAuthSerializer
from .models import ManagerMemo

class ManagerMemoSerializer(serializers.ModelSerializer):
    user     = UserAuthSerializer()

    class Meta:
        model = ManagerMemo
        fields = [
            'id'
            , 'target_id'
            , 'user'
            , 'memo'
            , 'created_at'
        ]

class ManagerMemoCreateSerializer(serializers.Serializer):
    target_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    memo = serializers.CharField()

    def create(self, validated_data):
        target_id = validated_data['target_id']
        user_id = validated_data['user_id']
        memo = validated_data['memo']

        memo_obj = ManagerMemo(
            target_id = target_id
            , user_id = user_id
            , memo = memo
        )

        memo_obj.save()
        return memo_obj