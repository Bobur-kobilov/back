import pytz, pymongo
import operator
from functools                  import reduce
from django.conf                import settings
from django.db.models           import Count, Sum, Q
from django.shortcuts           import render
from django.core.cache          import cache
from rest_framework             import status, viewsets
from rest_framework.response    import Response
from rest_framework.decorators  import list_route
from rest_framework.generics    import ListAPIView, UpdateAPIView
from rest_framework.views       import APIView
from rest_framework.decorators  import api_view, permission_classes

from becoin.model               import (
    Members
    , Accounts
    , SignupHistories
    , AccountVersions
    , Referrals
    , ReferralFriends
    , ReferralFeeHistories
    , ReferralInfos
    , PaymentAddresses
    , Orders
    , StopOrders
    , Withdraws
    , SignupHistories
    , TwoFactors
)
from bcoffice.message           import ResponseMessage
from bcoffice                   import constants
from bcoffice.constants         import currencyDic
from bcoffice.queue             import (
    QueueUtil
    , CENTRAL_LOGGING
    , TBL_BCOFFICE_MEMBER_MOD
    , TBL_BCOFFICE_REFERRAL_FEE_MOD
    , TBL_BCOFFICE_MODIFY_COIN_AMOUNT
)
from bcoffice.mongo_blacklist   import BCOfficeBlackListMongoDB
from bcoffice.mongo_history     import BCOfficeHistoryMongoDB
from bcoffice.logging           import CentralLogging, CREATE, UPDATE, DELETE, READ
from bcoffice.generics          import RawQueryListAPIView, RawQuerySyntax
from bcoffice.pagination        import RawQuerySetPagination, StandardPagination
from bcoffice.api_service       import APIService
from bcoffice.utils             import date_util, string_utils
from bcoffice.utils.date_util   import set_time_zone

from members.serializers import *
from members.permissions import *

from supports.models import Question
from becoin.model               import Members, Deposits, Withdraws, PaymentAddresses, Accounts

from account.models import User
from bcoffice.logging import CentralLogging, CREATE, UPDATE, DELETE, READ
from bcoffice.utils import logging_utils
from bcoffice.utils.valuation_utils import ValuationAssetsUtil
from datetime                   import datetime
from pytz import timezone
import json, ctypes


from .member_list                   import MemberList
from .member_detail                 import MemberDetail
from .member_balance_list           import MemberBalanceList
from .member_account_history_list   import MemberAccountHistoryList
from .member_modify_history_list    import MemberModifyHistoryList
from .member_active_history_list    import MemberActiveHistoryList
from .referral_common_value         import ReferralCommonValue
from .member_referral_list          import MemberReferralList
from .member_referral_pay_list      import MemberReferralPayList
from .member_referral_fee_list      import MemberReferralFeeList
from .locked_reason                 import LockedReasonAPI
from .member_search                 import MemberSearch
from .modify_coin_amount            import ModifyCoinAmount
from .modify_coin_amount_list       import ModifyCoinAmountList
from .member_force_disable import MemberForceDisable