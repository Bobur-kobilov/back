from django.conf.urls   import url
from .views import *

urlpatterns = [
    url(r'^v1/coin-account/balance/$',                              CoinBalanceList.as_view()                   , name=CoinBalanceList.name),                   # 암호화폐 잔고조회

    url(r'^v1/coin-account/deposit-history/$',                      CoinDepositHistoryList.as_view()            , name=CoinDepositHistoryList.name),            # 암호화폐 입금내역 조회

    url(r'^v1/coin-account/withdraw-confirm/$',                     WithdrawConfirmCreate.as_view()             , name=WithdrawConfirmCreate.name),                # 수동출금 승인
    url(r'^v1/coin-account/withdraw-cancel/$', WithdrawCancel.as_view(), name=WithdrawCancel.name),  # 수동출금 취소
    url(r'^v1/coin-account/withdraw-history/$',                     CoinWithdrawHistoryList.as_view()           , name=CoinWithdrawHistoryList.name),           # 암호화폐 출금내역 조회
    url(r'^v1/coin-account/withdraw-history/(?P<pk>[0-9]+)/$',      CoinWithdrawHistoryDetail.as_view()         , name=CoinWithdrawHistoryList.name),           # 암호화폐 출금내역 상세조회
    
    url(r'^v1/coin-account/withdraw-apply-reason/$',                WithdrawApplyReason.as_view()               , name=WithdrawApplyReason.name),   # 출금요청사유
    url(r'^v1/coin-account/withdraw-apply/$',                       WithdrawApplyList.as_view()                 , name=WithdrawApplyList.name), # 출금 요청 / 출금 요청 목록
    url(r'^v1/coin-account/hot-withdraw-apply/(?P<pk>[0-9]+)/$',    HotWithdrawApplyUpdate.as_view()            , name=HotWithdrawApplyUpdate.name), # 핫 월렛 출금 상태 수정
    url(r'^v1/coin-account/cold-withdraw-apply/(?P<pk>[0-9]+)/$',   ColdWithdrawApplyUpdate.as_view()           , name=ColdWithdrawApplyUpdate.name), # 콜드 월렛 출금 상태 수정
    url(r'^v1/coin-account/exchange-withdraw-history/$',            WithdrawHistoryList.as_view()               , name=WithdrawHistoryList.name), # 출금 요청 이력
    url(r'^v1/coin-account/withdraw-txid-update/$',                 ColdWithdrawTxidUpdate.as_view()            , name=ColdWithdrawTxidUpdate.name), # 콜드 월렛 출금 txid 수정

    url(r'^v1/coin-account/coldwallet-balance-update/$',            ColdwalletBalanceUpdate.as_view()           , name=CoinBalanceList.name),  # 콜드월렛 레디스 잔고 수정

    url(r'^v1/coin-account/daily-deposits-withdraws/$',             DailyDepositWithdrawList.as_view()          , name=DailyDepositWithdrawList.name),  # 일자별 입출금 내역
    url(r'^v1/coin-account/daily-total-sales/$',                    DailyTotalSalesList.as_view()               , name=DailyTotalSalesList.name),  # 일자별 매출액
    url(r'^v1/coin-account/daily-total-sales-csv/$',                DailyTotalSalesListCSV.as_view()            , name=DailyTotalSalesListCSV.name),  # 일자별 매출액 CSV   
    url(r'^v1/coin-account/daily-total-sales-csv-usd/$',            DailyTotalSalesListCSVUSD.as_view()         , name=DailyTotalSalesListCSVUSD.name),  # 일자별 매출액 CSV USD only  
    url(r'^v1/coin-account/user-activity/$',                        UserActivity.as_view()                      , name=UserActivity.name),  # 일자별 매출액 CSV USD only  
    url(r'^v1/coin-account/hold-list/$',                            HoldList.as_view()                          , name=HoldList.name), 
    url(r'^v1/coin-account/confirm-manual/$',                       ManualConfirm.as_view()                     , name=ManualConfirm.name),  
]
