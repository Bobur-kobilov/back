from django.db import models
from account.models import (
    User
)
"""
시스템 메시지 전송방식 설정 테이블
"""
class SystemAlarm(models.Model):
    id          = models.BigAutoField(primary_key=True)

    """
    회원가입 : 0000
    인증 - SMS, OTP : 0100
    로그인 - 일반 로그인 : 0200
    로그인 - IP변경 : 0201
    입금 - 완료 : 0300
    출금 - 신청 : 0400
    출금 - 완료 : 0401
    1:1문의 - 답변 : 0500
    공지 - 긴급공지 : 0600
    """
    alarm_code  = models.CharField(max_length=5, null=False, blank=False, unique=True)
    is_sms      = models.BooleanField(null=False, default=False)
    is_email    = models.BooleanField(null=False, default=False)

    class Meta:
        db_table = 'system_alarm'

class DepositAddress(models.Model):
    id              = models.BigAutoField(primary_key=True)
    author          = models.ForeignKey(User, related_name='author', on_delete=models.CASCADE)
    currency        = models.IntegerField(null=False)
    address_type    = models.CharField(max_length=20, null=False, blank=False, default="INSIDE") # 내부 : INSIDE, 외부 : OUTSIDE
    wallet_type     = models.CharField(max_length=4, null=True, blank=True)
    address         = models.CharField(max_length=255, null=False, blank=False)
    nick            = models.CharField(max_length=255, null=True, blank=True)
    tag             = models.CharField(max_length=255, null=True, blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'deposit_address'


class WalletRule(models.Model):
    id = models.BigAutoField(primary_key=True)
    currency = models.IntegerField(null=False)
    target_rate = models.FloatField(null=False)

    @staticmethod
    def findByCurrency(walletRule, currency):
        for rule in walletRule:
            if rule.currency == currency:
                return rule

        return None

    class Meta:
        db_table = 'wallet_rule'
