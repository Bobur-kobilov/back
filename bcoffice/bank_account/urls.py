from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^v1/bank-account/balance/$'               , BankBalanceList.as_view()             , name=BankBalanceList.name),           # KRW 잔고조회
    url(r'^v1/bank-account/deposit-history/$'       , BankDepositHistoryList.as_view()      , name=BankDepositHistoryList.name),    # KRW 입금내역조회
    url(r'^v1/bank-account/withdraw-history/$'      , BankWithdrawHistoryList.as_view()     , name=BankWithdrawHistoryList.name),   # KRW 입출금내역조회
]
