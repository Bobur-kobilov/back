from django.conf.urls   import url
from .views import *

urlpatterns = [
    url(r'^v1/security-level-policy/$'                  , SecurityLevelPolicy.as_view()             , name=SecurityLevelPolicy.name) # 등급별 출금한도 조회
    , url(r'^v1/security-level-policy/histories/$'        , SecurityLevelPolicyHistory.as_view()      , name=SecurityLevelPolicyHistory.name) # 등급별 출금한도 수정이력

    , url(r'^v1/system-alarm/$'                         , SystemAlarmListView.as_view()             , name=SystemAlarmListView.name) # 시스템 메시지 알림 목록
    , url(r'^v1/system-alarm/item/$'                    , SystemAlarmItemView.as_view()             , name=SystemAlarmListView.name) # 시스템 메시지 알림 아이템
    , url(r'^v1/system-alarm/update/$'                  , SystemAlarmUpdateView.as_view()           , name=SystemAlarmUpdateView.name) # 시스템 메시지 알림 설정 수정
    , url(r'^v1/referral-commission/$'                  , ReferralCommission.as_view()              , name=ReferralCommission.name) # 공통 커미션 비율
    , url(r'^v1/referral-commission/histories/$'        , ReferralCommissionHistory.as_view()       , name=ReferralCommissionHistory.name) # 공통 커미션 비율 변경 이력
    , url(r'^v1/tag-coins/$'                            , TagCoinList.as_view()                     , name=TagCoinList.name)
    , url(r'^v1/deposit-address/$'                      , DepositAddressList.as_view()              , name=DepositAddressList.name) #입금주소 관리
    , url(r'^v1/deposit-address/create/$'               , DepositAddressCreate.as_view()            , name=DepositAddressCreate.name) #입금주소 생성
    , url(r'^v1/deposit-address/(?P<pk>[0-9]+)/$'       , DepositAddressRetrieveDestroy.as_view()   , name=DepositAddressRetrieveDestroy.name) #입금주소 조회 및 삭제
    , url(r'^v1/wallet-rule/$'                          , WalletRuleList.as_view()                  , name=WalletRuleList.name) #지갑관리규칙
    , url(r'^v1/wallet-rule/(?P<pk>[0-9]+)/$'           , WalletRuleUpdate.as_view()                , name=WalletRuleUpdate.name)
    , url(r'^v1/market-management/$', MarketManagement.as_view(), name=MarketManagement.name) # 마켓별 매도가격 제한
]
