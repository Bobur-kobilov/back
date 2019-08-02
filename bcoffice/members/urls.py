from django.conf.urls   import url

from members import views
from .views import *

urlpatterns = [
    url(r'^v1/member-search/$'                    , MemberSearch.as_view()                      , name=MemberSearch.name),              # 거래소 유저 검색
    url(r'^v1/member-list/$'                    , MemberList.as_view()                      , name=MemberList.name),                    # 거래소 유저 목록 가져오기
    url(r'^v1/member-detail/$'                  , MemberDetail.as_view()                    , name=MemberDetail.name),                  # 거래소 유저 목록 가져오기
    # url(r'^v1/member/(?P<pk>[0-9]+)/$'          , MemberUpdate.as_view()                    , name=MemberUpdate.name),                # 거래소 유저 정보 수정

    url(r'^v1/member/balance/$'                 , MemberBalanceList.as_view()               , name=MemberBalanceList.name),             # 거래소 유저 잔고조회

    url(r'^v1/member/account-history/$'         , MemberAccountHistoryList.as_view()        , name=MemberAccountHistoryList.name),      # 거래소 유저 자산변동이력

    url(r'^v1/member/active-history/$'          , MemberActiveHistoryList.as_view()         , name=MemberActiveHistoryList.name),       # 거래소 유저 활동내역 가져오기

    url(r'^v1/member/modify-history/$'          , MemberModifyHistoryList.as_view()         , name=MemberModifyHistoryList.name),     # 거래소 유저 정보정정내역 가져오기
    
    url(r'^v1/member/referral-common/$'         , ReferralCommonValue.as_view()             , name = ReferralCommonValue.name),         # 추천인정보 상단
    url(r'^v1/member/referral-list/$'           , MemberReferralList.as_view()              , name = MemberReferralList.name),          # 추천인정보 피추천인
    url(r'^v1/member/referral-payments/$'       , MemberReferralPayList.as_view()           , name = MemberReferralPayList.name),       # 추천인정보 지급내역
    url(r'^v1/member/referral-fee/$'            , MemberReferralFeeList.as_view()           , name = MemberReferralFeeList.name),       # 추천인정보 수수료 변경내역
    url(r'^v1/member/modify-coin-amount/$'      , ModifyCoinAmount.as_view()                , name = ModifyCoinAmount.name),            # 회원 코인수량 정정
    url(r'^v1/member/modify-coin-amount-list/$' , ModifyCoinAmountList.as_view()            , name = ModifyCoinAmountList.name),        # 회원 코인수량 정정이력

    url(r'^v1/member/locked-reason/$'          , LockedReasonAPI.as_view()                  , name = LockedReasonAPI.name),             # 동결사유 내역

    url(r'^v1/member/factor_auth/$'            , MemberForceDisable.as_view(), name=MemberForceDisable.name ), # Two Factor 인증 비활성
    url(r'^v1/member/kyc_auth/$'               , MemberForceDisable.as_view(), name=MemberForceDisable.name  ), # 신분증 인증 활성, 비활성화
    url(r'^v1/member/disable/$'                , MemberForceDisable.as_view(), name=MemberForceDisable.name  ), # 계정비활성화 인증 활성, 비활성화
    url(r'^v1/member/restrict/$'               , MemberForceDisable.as_view(), name=MemberForceDisable.name  ), # 이용제한 인증 활성, 비활성화
    url(r'^v1/member/deleted/$'                , MemberForceDisable.as_view(), name=MemberForceDisable.name  ), # 탈퇴처리
]
