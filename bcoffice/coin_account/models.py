from django.db import models
from policy_manage.models import DepositAddress
from account.models import User

# Create your models here.
class DepositsAdd(models.Model):
    account_id = models.IntegerField(blank=True, null=True)
    member_id = models.IntegerField(blank=True, null=True)
    currency = models.IntegerField(blank=True, null=True)
    amount = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    fee = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    fund_uid = models.CharField(max_length=255, blank=True, null=True)
    fund_extra = models.CharField(max_length=255, blank=True, null=True)
    txid = models.CharField(max_length=255, blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)
    aasm_state = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    done_at = models.DateTimeField(blank=True, null=True)
    confirmations = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    payment_transaction_id = models.IntegerField(blank=True, null=True)
    txout = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False

class WithdrawReason(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=50, blank=False, null=False)
    description = models.CharField(max_length=100, blank=False, null=False)
    reason_type = models.CharField(max_length=30, blank=False, null=False, default="HOT")

    class Meta:
        db_table = 'withdraw_reason'


class WithdrawApply(models.Model):
    """
    HOT/COLD 출금실행 테이블
    status
    - 100 : 대기
    - 200 : 승인
    - 300 : 거절
    """
    id                  = models.BigAutoField(primary_key=True)
    wallet_type         = models.CharField(max_length=30, null=False, blank=False) # 지갑타입(HOT, COLD)
    currency            = models.IntegerField(blank=False, null=False) # 
    requester           = models.ForeignKey(User, related_name="requester", on_delete=models.CASCADE) # 요청자
    supervisor          = models.BigIntegerField(blank=True, null=True, default=-1) # 처리자
    withdraw_wallet     = models.ForeignKey(DepositAddress, related_name="withdraw_wallet", on_delete=models.CASCADE) # 출금지갑
    deposit_wallet      = models.ForeignKey(DepositAddress, related_name="deposit_wallet", on_delete=models.CASCADE) # 입금지갑
    withdraw_volume     = models.FloatField(blank=False, null=False, default=0) # 출금수량
    reason              = models.ForeignKey(WithdrawReason, related_name="reason", on_delete=models.CASCADE) # 출금사유
    etc_reason          = models.CharField(max_length=255, blank=True, null=True) # 기타사유
    created_at          = models.DateTimeField(auto_now_add=True) # 레코드 생성일
    updated_at          = models.DateTimeField(auto_now=True) # 레코드 수정일
    proc_date           = models.DateTimeField(blank=True, null=True) # 처리일
    status              = models.IntegerField(blank=False, null=False, default=100) # 상태값

    class Meta:
        db_table = 'withdraw_apply'


class WithdrawHistory(models.Model):
    """
    거래소 출금 내역 조회
    deal_type
    - 100 : 출금
    - 200 : 입금
    """
    id              = models.BigAutoField(primary_key=True)
    withdraw_apply  = models.ForeignKey(WithdrawApply, related_name="withdraw_apply_info", on_delete=models.CASCADE)
    supervisor      = models.ForeignKey(User, related_name="supervisor_info", on_delete=models.CASCADE)
    requester       = models.ForeignKey(User, related_name="requester_info", on_delete=models.CASCADE)
    currency        = models.IntegerField(blank=False, null=False)
    deal_type       = models.IntegerField(blank=False, null=False) # 거래구분(100: 출금, 200:입금)
    volume          = models.FloatField(default=0)
    wallet          = models.ForeignKey(DepositAddress, related_name="wallet_address", on_delete=models.CASCADE)
    request_date    = models.DateTimeField(blank=False, null=False)
    approval_date   = models.DateTimeField(blank=False, null=False)
    created_at      = models.DateTimeField(auto_now_add=True)
    txid            = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'withdraw_history'


