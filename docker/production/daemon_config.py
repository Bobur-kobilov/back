SCHEDULER_START_NOW = True
BALANCE_COLLECT_PERIOD = 100

DATABASE = {
    'NAME': 'chainbboffice',
    'USER': 'chainbback',
    'PASSWORD': 'Vp9dlsb025',
    'HOST': 'prod-chainb-backoffice.cluster-c96sjzsh7dzo.ap-northeast-2.rds.amazonaws.com',
    'PORT': '3306'
}

REDIS = {
    'HOST': 'prod-chainb-single.tfp4ss.ng.0001.apn2.cache.amazonaws.com'
    , 'PORT': '6379'
}

COIN_MANAGER_ADDRESS = 'http://internal-prod-chainb-coinmanager-1214697675.ap-northeast-2.elb.amazonaws.com:3001'

IS_TESTNET = False

MAIN_NET_COIN_API = {
    'BTC'       : 'https://api.blockcypher.com/v1/btc/main/addrs/{0}/balance'
    #, 'QTUM'    : 'https://explorer.qtum.org/insight-api/erc20/balances?balanceAddress={0}'
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

BACKOFFICE_BACKEND_HOST = 'http://admin.chainb.io'
CURRENCY_LIST_API = '/v1/get-currency-list/'