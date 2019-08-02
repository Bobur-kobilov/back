from datetime                   import datetime
from pytz import timezone
import json, pytz, re, pymongo

from django.conf                import settings
from django.core.cache          import cache
from django.shortcuts           import render
from django.db.models           import Count
from rest_framework             import mixins, status
from rest_framework.generics    import CreateAPIView, RetrieveAPIView, ListAPIView, ListCreateAPIView, RetrieveDestroyAPIView, UpdateAPIView
from rest_framework.pagination  import LimitOffsetPagination
from rest_framework.response    import Response
from rest_framework.views       import APIView

from bcoffice                   import constants
from bcoffice.api_service       import APIService
from bcoffice.message           import ResponseMessage
from bcoffice.utils             import date_util

from becoin.model               import (
    ReferralInfos
)

from bcoffice.utils.valuation_utils import ValuationAssetsUtil
from bcoffice.api_service           import APIService
from bcoffice.logging               import CentralLogging, CREATE, UPDATE, DELETE, READ
from bcoffice.utils                 import logging_utils
from bcoffice.mongo_history                 import BCOfficeHistoryMongoDB
from bcoffice.coin_manager          import CoinManager
from bcoffice.queue import (
    QueueUtil
    , TBL_BCOFFICE_DEPOSIT_WITHDRAW_MOD
    , TBL_BCOFFICE_REFERRAL_COMMISSION_MOD
)

from account.models import User
from policy_manage.permissions import *
from policy_manage.models import *
from policy_manage.serializers import *

from .security_level_policy         import SecurityLevelPolicy
from .security_level_policy_history import SecurityLevelPolicyHistory
from .system_alarm_list             import SystemAlarmListView
from .system_alarm_item             import SystemAlarmItemView
from .system_alarm_update           import SystemAlarmUpdateView
from .referral_commission           import ReferralCommission
from .referral_commission_history   import ReferralCommissionHistory
from .deposit_address_list          import DepositAddressList
from .deposit_address_create        import DepositAddressCreate
from .deposit_address_retrieve_destroy import DepositAddressRetrieveDestroy
from .tag_coin_list                 import TagCoinList
from .wallet_rule_list              import WalletRuleList
from .wallet_rule_update            import WalletRuleUpdate
from .market_management import MarketManagement