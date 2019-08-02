import os, pymongo
from django.db.models import Sum, Count, Q
from django.db import connections
from django.conf import settings

from rest_framework             import status
from rest_framework.generics    import ListAPIView
from rest_framework.views       import APIView
from rest_framework.response    import Response
from rest_framework.pagination  import LimitOffsetPagination

from trend.permissions import *

from becoin.model               import Orders, Trades, Deposits, Withdraws, SignupHistories, Members, ReferralFeeHistories, Referrals

from bcoffice.utils.date_util   import set_time_zone
from bcoffice.message           import ResponseMessage
from bcoffice.pagination        import StandardPagination
from bcoffice.mongo             import BCOfficeMongoDB
from bcoffice.queue import (
    TBL_BCOFFICE_COIN_TRANSACTION_STATUS,
    TBL_BCOFFICE_TRADE_OPERATIONS,
    TBL_BCOFFICE_REFERRAL_STATUS
)

from datetime                   import datetime, timedelta
from pytz                       import timezone

from .trend_list import TrendList
from .coin_transaction_status import CoinTransactionStatusList
from .trade_operations import TradeOperationsList
from .referral_status import ReferralStatusList