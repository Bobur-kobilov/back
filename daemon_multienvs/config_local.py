SCHEDULER_START_NOW = True
BALANCE_COLLECT_PERIOD = 300

DATABASE = {    
    'NAME': 'devoffice',
    'USER': 'devpub',
    'PASSWORD': '21Cpdlsb96',
    'HOST': 'dev-chainb-exchange-pub.c96sjzsh7dzo.ap-northeast-2.rds.amazonaws.com',
    'PORT': '3306',
    'OPTIONS': {
        'init_command': "SET " +
            "sql_mode='STRICT_TRANS_TABLES'," +
            "MAX_EXECUTION_TIME=15000," +
            "character_set_connection=utf8," +
            "collation_connection=utf8_unicode_ci",
        'connect_timeout': 30
    }
}

REDIS = {
    'HOST': '13.124.120.100'
    , 'PORT': '6379'
}

COIN_MANAGER_ADDRESS = 'http://10.30.0.239:3002'

IS_TESTNET = True

MAIN_NET_COIN_API = {
    'BTC'       : 'https://api.blockcypher.com/v1/btc/main/addrs/{0}/balance'    
    , 'QTUM'    : 'https://explorer.qtum.org/insight-api/addr/{0}/balance'
    , 'BCH'     : 'https://blockdozer.com/insight-api/addr/{0}/balance'
    , 'ADA'     : 'https://cardanoexplorer.com/api/addresses/summary/{0}'
}

TEST_NET_COIN_API = {
    'BTC'       : 'https://testnet.blockexplorer.com/api/addr/{0}'
    , 'ETH'     : 'https://api-ropsten.etherscan.io/api?module=account&action=balance&address={0}'
    , 'QTUM'    : 'https://testnet.qtum.org/insight-api/addr/{0}/?noTxList=1'
    , 'BCH'     : 'https://bch-insight.bitpay.com/api/addr/{0}'
}

BACKOFFICE_BACKEND_HOST = 'http://127.0.0.1:4200'
CURRENCY_LIST_API = '/v1/get-currency-list/'