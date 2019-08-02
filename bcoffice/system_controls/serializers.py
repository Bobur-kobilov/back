from rest_framework import serializers

from .models import MtsVersion


# 주문내역 시리얼라이저
class MtsVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MtsVersion
        fields = [
            'id'
            , 'version'
            , 'device'
        ]