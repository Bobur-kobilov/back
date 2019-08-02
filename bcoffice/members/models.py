from django.db import models

# Create your models here.

# 추천인정보 테이블
class ReferralList(models.Model):
    referral_id = models.IntegerField(blank=True, null=True)
    member_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    display_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False