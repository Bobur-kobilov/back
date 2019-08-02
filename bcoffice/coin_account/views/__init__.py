import pymongo
from decimal import Decimal
from django.db.models   import Sum, Count, Q
from django.shortcuts   import render
from django.core.cache  import cache
from django.db.models.sql.query import RawQuery
from django.db.models.query     import RawQuerySet
from rest_framework             import status, viewsets
from rest_framework.generics    import ListAPIView, CreateAPIView, RetrieveAPIView, ListCreateAPIView, UpdateAPIView
from rest_framework.views       import APIView
from rest_framework.pagination  import LimitOffsetPagination
from rest_framework.response    import Response
from rest_framework.renderers   import BaseRenderer
from rest_framework.decorators  import list_route
from rest_framework_csv.renderers import CSVRenderer

from coin_account.serializers               import *
from coin_account.permissions               import *

from coin_account.models import (
    WithdrawApply
    , WithdrawReason
    , WithdrawHistory
)

from account.models             import User
from account.serializers        import UserAuthSerializer
from bcoffice.coin_manager      import CoinManager
from becoin.model               import Accounts, Deposits, Withdraws, Members, Trades, ReferralFeeHistories
from policy_manage.models       import WalletRule, DepositAddress

from bcoffice.api_service       import APIService
from bcoffice.utils.valuation_utils import ValuationAssetsUtil
from bcoffice.message           import ResponseMessage
from bcoffice.generics          import RawQueryListAPIView, RawQuerySyntax
from bcoffice.pagination        import RawQuerySetPagination, StandardPagination
from bcoffice.utils             import string_utils
from bcoffice.utils.coin_util   import CoinUtil
from bcoffice.utils.date_util   import set_time_zone
from bcoffice                   import constants
from bcoffice.constants         import currencyDic
from bcoffice.mongo             import BCOfficeMongoDB
from bcoffice.mongo_history     import BCOfficeHistoryMongoDB
from bcoffice.logging           import CentralLogging, UPDATE, CREATE
from bcoffice.utils             import logging_utils
from bcoffice.queue import (
    TBL_BCOFFICE_WITHDRAW_CONFIRM
    , TBL_BCOFFICE_WITHDRAW_CANCEL
    , TBL_BCOFFICE_DAILY_DEPOSIT_WITHDRAW
    , TBL_BCOFFICE_DAILY_TOTAL_SALES
)
from django.conf                import settings
from datetime                   import datetime, timedelta
from pytz                       import timezone
from bcoffice.utils             import mq_utils

from .coin_balance_list import CoinBalanceList
from .coin_deposit_history import CoinDepositHistoryList
from .coin_withdraw_history_list import CoinWithdrawHistoryList
from .coin_withdraw_history_detail import CoinWithdrawHistoryDetail
from .withdraw_apply_reason import WithdrawApplyReason
from .withdraw_apply_list import WithdrawApplyList
from .hot_withdraw_apply_update import HotWithdrawApplyUpdate
from .cold_withdraw_apply_update import ColdWithdrawApplyUpdate
from .cold_withdraw_txid_update import ColdWithdrawTxidUpdate
from .withdraw_history_list import WithdrawHistoryList
from .withdraw_confirm_create import WithdrawConfirmCreate
from .coldwallet_balance_update import ColdwalletBalanceUpdate
from .daily_deposit_withdraw import DailyDepositWithdrawList
from .daily_total_sales import DailyTotalSalesList, DailyTotalSalesListCSV, DailyTotalSalesListCSVUSD
from .withdraw_cancel import WithdrawCancel
from .user_activity import UserActivity
from .hold_list import HoldList
from .manual_confirm import ManualConfirm