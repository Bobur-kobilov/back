from django.db import models

# Create your models here.

# 체결내역 통합 테이블 (체결내역 + 매수주문내역 + 매도주문내역)
class OrderDone(models.Model):
    bid_ask = models.IntegerField(blank=True, null=True)
    bid_bid = models.IntegerField(blank=True, null=True)
    ask_bid = models.IntegerField(blank=True, null=True)
    ask_ask = models.IntegerField(blank=True, null=True)
    trd_currency = models.IntegerField(blank=True, null=True)
    trd_price = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    trd_volume = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    trd_funds = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    trd_trend = models.IntegerField(blank=True, null=True)
    trd_created_at = models.DateTimeField(blank=True, null=True)
    bid_id = models.IntegerField(blank=True, null=True)
    bid_member_id = models.IntegerField(blank=True, null=True)
    bid_price = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    bid_origin_volume = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    trd_bid_fee = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    bid_created_at = models.DateTimeField(blank=True, null=True)
    ask_id = models.IntegerField(blank=True, null=True)
    ask_member_id = models.IntegerField(blank=True, null=True)
    ask_price = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    ask_origin_volume = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    trd_ask_fee = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    ask_created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False


# 상세주문내역 통합 테이블 (주문내역 + 체결내역 + stop주문내역)
class OrderDetail(models.Model):
    o_member_id = models.IntegerField(blank=True, null=True)
    o_origin_id = models.IntegerField(blank=True, null=True)
    o_first_id = models.IntegerField(blank=True, null=True)
    t_id = models.IntegerField(blank=True, null=True)
    o_state = models.IntegerField(blank=True, null=True)
    o_bid = models.IntegerField(blank=True, null=True)
    o_ask = models.IntegerField(blank=True, null=True)
    o_currency = models.IntegerField(blank=True, null=True)
    o_type = models.CharField(max_length=8, blank=True, null=True)
    o_ord_type = models.CharField(max_length=10, blank=True, null=True)
    o_source = models.CharField(max_length=255)
    o_origin_volume = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    o_volume = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    o_price = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    o_locked = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    o_origin_locked = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    s_price = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    t_bid_id = models.IntegerField(blank=True, null=True)
    t_ask_id = models.IntegerField(blank=True, null=True)
    t_price = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    t_volume = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    t_remain_volume = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    t_funds = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    t_bid_fee = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    t_ask_fee = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    s_created_at = models.DateTimeField(blank=True, null=True)
    o_created_at = models.DateTimeField(blank=True, null=True)
    t_created_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        managed = False