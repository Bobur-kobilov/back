from django.conf.urls   import url
from .views           import *

urlpatterns = [
    url(r'^v1/order_history/done/$',                            OrderDoneList.as_view(),            name=OrderDoneList.name),           # 체결내역조회
    url(r'^v1/order_history/stop/$',                            OrderStopList.as_view(),            name=OrderStopList.name),           # Stop주문내역조회
    url(r'^v1/order_history/detail/$',                          OrderDetailList.as_view(),          name=OrderDetailList.name),         # 상세주문내역조회
    url(r'^v1/order_history/list/$',                            OrderList.as_view(),                name=OrderList.name),               # 주문내역조회

    url(r'^v1/order_history/force-cancel/$',                    OrderForceCancel.as_view(),        name=OrderForceCancel.name),         # 주문내역 강제취소
]