from django.conf.urls   import url
from .views           import *

urlpatterns = [
    url(r'^v1/trend/list/$',                            TrendList.as_view(),            name=TrendList.name),           # 트랜드 내역 조회
    url(r'^v1/trend/coin-transaction-status/$', CoinTransactionStatusList.as_view(), name=CoinTransactionStatusList.name), # 코인별 거래현황
    url(r'^v1/trend/trade-operations/$', TradeOperationsList.as_view(), name=TradeOperationsList.name), # 거래 운영
    url(r'^v1/trend/referrals-status/$', ReferralStatusList.as_view(), name=ReferralStatusList.name), # 레퍼럴 현황
]