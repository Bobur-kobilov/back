from rest_framework import serializers

from becoin.model import Orders, Trades, StopOrders
from .models import OrderDone, OrderDetail


# 주문내역 시리얼라이저
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = [
            'id'
            , 'bid'
            , 'ask'
            , 'currency'
            , 'price'
            , 'volume'
            , 'origin_volume'
            , 'state'
            , 'type'
            , 'member_id'
            , 'created_at'
            , 'updated_at'
            , 'source'
            , 'ord_type'
            , 'locked'
            , 'origin_locked'
            , 'funds_received'
            , 'trades_count'
            , 'amount'
            , 'origin_id'
            , 'first_id'
        ]


# 체결내역 시리얼라이저
class TradesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDone
        fields = [
            'id'
            , 'bid_ask'
            , 'bid_bid'
            , 'ask_bid'
            , 'ask_ask'
            , 'trd_currency'
            , 'trd_price'
            , 'trd_volume'
            , 'trd_funds'
            , 'trd_trend'
            , 'trd_created_at'
            , 'bid_id'
            , 'bid_member_id'
            , 'bid_price'
            , 'bid_origin_volume'
            , 'trd_bid_fee'
            , 'bid_created_at'
            , 'ask_id'
            , 'ask_member_id'
            , 'ask_price'
            , 'ask_origin_volume'
            , 'trd_ask_fee'
            , 'ask_created_at'
        ]


# 상세주문내역 시리얼라이저
class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = [
            'id'
            , 'o_member_id'
            , 'o_origin_id'
            , 'o_first_id'
            , 't_id'
            , 'o_state'
            , 'o_type'
            , 'o_bid'
            , 'o_ask'
            , 'o_currency'
            , 'o_ord_type'
            , 'o_source'
            , 'o_origin_volume'
            , 'o_volume'
            , 'o_price'
            , 'o_locked'
            , 'o_origin_locked'
            , 's_price'
            , 't_bid_id'
            , 't_ask_id'
            , 't_price'
            , 't_volume'
            , 't_remain_volume'
            , 't_funds'
            , 't_bid_fee'
            , 't_ask_fee'
            , 's_created_at'
            , 'o_created_at'
            , 't_created_at'
        ]


# Stop주문내역 시리얼라이저
class StopOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = StopOrders
        fields = [
            'id'        
            , 'bid'
            , 'ask'
            , 'currency'
            , 'price'
            , 'volume'
            , 'state'
            , 'done_at'
            , 'type'
            , 'member_id'
            , 'created_at'
            , 'updated_at'
            , 'ord_type'
            , 'target_price'
            , 'locked'
            , 'amount'
            , 'order_id'
            , 'source'
        ]