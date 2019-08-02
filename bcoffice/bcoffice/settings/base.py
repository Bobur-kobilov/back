import os
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'f8cff66ee6fd4690b214c65c7ed4c3ed302077a3-8725-4af4-acc6-3ef0b1554c73'

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin'
    , 'django.contrib.auth'
    , 'django.contrib.contenttypes'
    , 'django.contrib.sessions'
    , 'django.contrib.messages'
    , 'django.contrib.staticfiles'
    , 'rest_framework'
    , 'corsheaders'
    , 'becoin'
    , 'account.apps.AccountConfig'
    , 'members.apps.MembersConfig'
    , 'bank_account.apps.BankAccountConfig'
    , 'coin_account.apps.CoinAccountConfig'
    , 'boards.apps.BoardsConfig'
    , 'order_history.apps.OrderHistoryConfig'
    , 'supports.apps.SupportsConfig'
    , 'manager_memo.apps.ManagerMemoConfig'
    , 'policy_manage.apps.PolicyManageConfig'
    , 'system_controls.apps.SystemControlsConfig'
    , 'storages'
    , 'trend.apps.TrendConfig'
]

AUTH_USER_MODEL = 'account.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
#    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'bcoffice.middleware.BackofficeCommonLoggingMiddleware'
]

ROOT_URLCONF = 'bcoffice.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/
LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATIC_URL = '/static/'

# ----------------
# For RestFul Apis
# ----------------
REST_FRAMEWORK = {
    'DATETIME_FORMAT': "%Y-%m-%d %H:%M:%S",
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS':
    'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': None,
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter'
    )
}

DEFAULT_PARSER_CLASSES = {
    'rest_framework.parsers.JSONParser',
    'rest_framework.parsers.FormParser',
    'rest_framework.parsers.MultiPartParser'
}

DEFAULT_RENDERER_CLASSES = {
    'rest_framework.renderers.JSONRenderer',
    'rest_framework.renderers.BrowsableAPIRenderer'
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(hours=8),
    'JWT_ALLOW_REFRESH': True,
    'JWT_GET_USER_SECRET_KEY': 'account.utils.get_secret_key',
    'JWT_VERIFY': True,
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'account.utils.jwt_response_payload_handler',
    'JWT_AUTH_HEADER_PREFIX': 'BCG'
}

CORS_ALLOW_CREDENTIALS = True
APPEND_SLASH = False