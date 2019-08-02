from .base import *
import urllib.request, json
import socket

ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True

DEBUG = True

USE_ETAGS = False

WSGI_APPLICATION = 'bcoffice.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'chainbboffice',
        'USER': 'chainsynco',
        'PASSWORD': '21Cpdlsb96',
        'HOST': 'prod-chainb-exchange.cluster-c96sjzsh7dzo.ap-northeast-2.rds.amazonaws.com',
        'PORT': '3306',
        'OPTIONS': {}
    },
    'exchange': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'chainbexchange',
        'USER': 'chainsynco',
        'PASSWORD': '21Cpdlsb96',
        'HOST': 'prod-chainb-exchange.cluster-c96sjzsh7dzo.ap-northeast-2.rds.amazonaws.com',
        'PORT': '3306',
        'OPTIONS': {}
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://prod-chainb.tfp4ss.ng.0001.apn2.cache.amazonaws.com:6379",
        "KEY_FUNCTION": "bcoffice.redis.key_prefix",
        "OPTIONS": {
            "CLIENT_CLASS": "bcoffice.redis.RedisCustomClient"
        }
    }
}

RABBIT_MQ = {
    'URL': '10.80.51.152'
	, 'PORT': 5672
    , 'USER': 'chainb'
    , 'PASSWORD': '21cpdlsQl'
}

MONGODB_DATABASES = {
    'default': {
        'HOST': '10.80.51.100'
        ,'HOST': '10.80.61.56'
        ,'HOST': '10.80.51.60'
        , 'PORT': 30000
        , 'NAME' : 'bcg_logging'
    },
    'blacklist': {
        'HOST': '10.80.51.100'
        ,'HOST': '10.80.61.56'
        ,'HOST': '10.80.51.60'
        , 'PORT': 30000
        , 'NAME' : 'bcg_blacklist'
    },
    'trend': {
        'HOST': '10.80.51.100'
        ,'HOST': '10.80.61.56'
        ,'HOST': '10.80.51.60'
        , 'PORT': 30000
        , 'NAME' : 'bcg_trend'
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'ERROR',
        },
    }
}

# = 'amqp://shkim:shkim@192.168.0.19'

S3_USE_SIGV4 = True

AWS_S3_OBJECT_PARAMETERS = {
    'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
    'CacheControl': 'max-age=94608000',
}

AWS_ACCESS_KEY_ID = "AKIAIMEOW6UUOQQ2ZMRQ"
AWS_SECRET_ACCESS_KEY = "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"
AWS_STORAGE_BUCKET_NAME = "exchange-syncodax"
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_REGION_NAME = "ap-northeast-2"
AWS_S3_CUSTOM_DOMAIN = 'd3eqlzg5jj4rap.cloudfront.net'

MEDIA_URL = "d3eqlzg5jj4rap.cloudfront.net/"

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

MAX_UPLOAD_SIZE = "5242880"
MAX_IMAGE_LENGTH = 20971520
# MEDIA_URL = '/upload/'
# MEDIA_ROOT = os.path.join('/06.Projects/BCG/BCOffice/', "upload")

EXCEL_CREATOR = 'SYNCO'
# UPLOAD_PROTOCOL = 'http'
# UPLOAD_IP_ADDRESS = '127.0.0.1'

API_PROTOCOL = 'http' # 거래소 API 프로토콜
API_HOST = 'internal-prod-chainb-bo-api-861422118.ap-northeast-2.elb.amazonaws.com' # 거래소 API 호스트 주소

MARKET_URL = "/api/v2/markets"
CURRENCY_URL = "/api/v2/currencies"

CURRENCY_LIST = []
MARKET_LIST = []

if CURRENCY_LIST.__len__() is 0 :
    currencies = urllib.request.urlopen(API_PROTOCOL + "://" + API_HOST + CURRENCY_URL)
    currencies_data = json.loads(currencies.read().decode())
    CURRENCY_LIST = currencies_data

if MARKET_LIST.__len__() is 0 :
    markets = urllib.request.urlopen(API_PROTOCOL + "://" + API_HOST + MARKET_URL)
    markets_data = json.loads(markets.read().decode())
    MARKET_LIST = markets_data


TAG_COINS = ['BCN', 'BTS', 'GXS', 'STEEM', 'XEM', 'XLM', 'XMR', 'XRP']


COIN_MANAGER_ADDRESS = 'http://internal-prod-chainb-coinmanager-1214697675.ap-northeast-2.elb.amazonaws.com:3001'

IS_TEST_NET = True

MAIN_NET_COIN_API = {
    'BTC'       : 'https://api.blockcypher.com/v1/btc/main/addrs/{0}/balance'
    , 'QTUM'    : 'https://explorer.qtum.org/insight-api/addr/{0}/?noTxList=1'
    , 'BCH'     : 'https://blockdozer.com/insight-api/addr/{0}/balance'
    , 'ADA'     : 'https://cardanoexplorer.com/api/addresses/summary/{0}'
}

TEST_NET_COIN_API = {
    'BTC'       : 'https://testnet.blockexplorer.com/api/addr/{0}'
    , 'ETH'     : 'https://api-ropsten.etherscan.io/api?module=account&action=balance&address={0}'
    , 'QTUM'    : 'https://testnet.qtum.org/insight-api/addr/{0}/?noTxList=1'
    , 'BCH'     : 'https://bch-insight.bitpay.com/api/addr/{0}'
}

DEFAULT_SUPER_USER = {
    'EMAIL' : 'administrator@domain.com'
    , 'PASSWORD' : 'superUser!!'
}

DEFAULT_DEPT_DUTY = {
    'duty_cd'           : '00'
    , 'duty_name'       : '관리자'
    , 'duty_eng_name'   : 'Administrator'
    , 'status'          : 'ACTV'
}

DEFAULT_DEPT_RANK = {
    'rank_cd'           : '00'
    , 'rank_name'       : '관리자'
    , 'rank_eng_name'   : 'Administrator'
    , 'status'          : 'ACTV'
}

DEFAULT_DEPT_TYPE = {
    'dept_cd'           : '00'
    , 'team_cd'         : '00'
    , 'dept_name'       : '관리부'
    , 'dept_eng_name'   : 'Management'
    , 'managerial'      : 1
    , 'status'          : 'ACTV'
}

DEFAULT_SYSTEM_ALARM = [
    {'alarm_code': '0000', 'is_sms': 1, 'is_email': 1}
    , {'alarm_code': '0100', 'is_sms': 0, 'is_email': 1}
    , {'alarm_code': '0200', 'is_sms': 0, 'is_email': 1}
    , {'alarm_code': '0201', 'is_sms': 1, 'is_email': 0}
    , {'alarm_code': '0300', 'is_sms': 1, 'is_email': 0}
    , {'alarm_code': '0400', 'is_sms': 0, 'is_email': 1}
    , {'alarm_code': '0401', 'is_sms': 0, 'is_email': 1}
    , {'alarm_code': '0500', 'is_sms': 1, 'is_email': 1}
    , {'alarm_code': '0600', 'is_sms': 0, 'is_email': 0}
]

"""
출금사유
"""
DEFAULT_WITHDRAW_REASON = [
    {'code': 100    , 'description': 'HOT비중초과'    , 'reason_type':'HOT'}
    , {'code': 150  , 'description': 'COLD비중초과'   , 'reason_type':'COLD'}
    , {'code': 200  , 'description': '오입금환불'     , 'reason_type':'HOT, COLD'}
    , {'code': 999  , 'description': '기타사유'       , 'reason_type':'HOT, COLD'}
]

"""
FAQ 카테고리
"""
DEFAULT_FAQ_CATEGORY = [
    {"category": "전체보기", "category_id": 1, "lang": "ko"}
    , {"category": "개인정보", "category_id": 2, "lang": "ko"}
    , {"category": "기타", "category_id": 3, "lang": "ko"}
    , {"category": "인증", "category_id": 4, "lang": "ko"}
    , {"category": "거래", "category_id": 5, "lang": "ko"}

    , {"category": "View all", "category_id": 1, "lang": "en"}
    , {"category": "Personal Information", "category_id": 2, "lang": "en"}
    , {"category": "etc.", "category_id": 3, "lang": "en"}
    , {"category": "Authentication", "category_id": 4, "lang": "en"}
    , {"category": "Trading", "category_id": 5, "lang": "en"}

    , {"category": "Xem toàn bộ", "category_id": 1, "lang": "vi"}
    , {"category": "Thông tin cá nhân", "category_id": 2, "lang": "vi"}
    , {"category": "Nội dung khác", "category_id": 3, "lang": "vi"}
    , {"category": "Xác nhận", "category_id": 4, "lang": "vi"}
    , {"category": "Giao dịch", "category_id": 5, "lang": "vi"}

    , {"category": "全体を見る", "category_id": 1, "lang": "ja"}
    , {"category": "個人情報", "category_id": 2, "lang": "ja"}
    , {"category": "その他", "category_id": 3, "lang": "ja"}
    , {"category": "認証", "category_id": 4, "lang": "ja"}
    , {"category": "取引", "category_id": 5, "lang": "ja"}

    , {"category": "查看全部", "category_id": 1, "lang": "zh-CN"}
    , {"category": "个人信息", "category_id": 2, "lang": "zh-CN"}
    , {"category": "其他", "category_id": 3, "lang": "zh-CN"}
    , {"category": "验证", "category_id": 4, "lang": "zh-CN"}
    , {"category": "交易", "category_id": 5, "lang": "zh-CN"}
]

"""
1:1 문의 카테고리
"""
DEFAULT_QUESTION_TYPE = [
    {"type": "계정", "category_id": 1, "lang": "ko"}
    , {"type": "매매", "category_id": 2, "lang": "ko"}
    , {"type": "오입금", "category_id": 3, "lang": "ko"}
    , {"type": "일반", "category_id": 4, "lang": "ko"}
    , {"type": "제안", "category_id": 5, "lang": "ko"}

    , {"type": "Account", "category_id": 1, "lang": "en"}
    , {"type": "Trading", "category_id": 2, "lang": "en"}
    , {"type": "Deposit Error", "category_id": 3, "lang": "en"}
    , {"type": "General Inquiry", "category_id": 4, "lang": "en"}
    , {"type": "Suggestions", "category_id": 5, "lang": "en"}

    , {"type": "Tài khoản", "category_id": 1, "lang": "vi"}
    , {"type": "Tiếp thị", "category_id": 2, "lang": "vi"}
    , {"type": "Nạp tiền sai", "category_id": 3, "lang": "vi"}
    , {"type": "Yêu cầu chung", "category_id": 4, "lang": "vi"}
    , {"type": "Đề xuất", "category_id": 5, "lang": "vi"}

    , {"type": "アカウント", "category_id": 1, "lang": "ja"}
    , {"type": "マーケティング", "category_id": 2, "lang": "ja"}
    , {"type": "誤入金", "category_id": 3, "lang": "ja"}
    , {"type": "一般", "category_id": 4, "lang": "ja"}
    , {"type": "提案", "category_id": 5, "lang": "ja"}

    , {"type": "帐户", "category_id": 1, "lang": "zh-CN"}
    , {"type": "市场", "category_id": 2, "lang": "zh-CN"}
    , {"type": "存款错误", "category_id": 3, "lang": "zh-CN"}
    , {"type": "一般", "category_id": 4, "lang": "zh-CN"}
    , {"type": "主张", "category_id": 5, "lang": "zh-CN"}
]

M2_MEMBER_ID_LIST = [43709, 43710, 43711, 43712, 43713, 62, 87, 88]

STATS_API_KEY = 'n8lzFtWXwJbeHxm1Cln1Oz7Imwlgs5Ng'