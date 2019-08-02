import logging, os, pymysql, requests, time
from logging.handlers import RotatingFileHandler
from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.background import BackgroundScheduler

from datetime import datetime
from redis import Redis, exceptions, RedisError
from redis.sentinel import (
    Sentinel
    , SentinelConnectionPool
    , ConnectionError
    , MasterNotFoundError
    , SlaveNotFoundError
)
import config
from coin_manager import CoinManager
from rest_framework.response import Response
from rest_framework import status

# create logger with 'spam_application'
logger = logging.getLogger('cold_wallet_logger')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)

if not os.path.exists('./logs'):
    os.makedirs("./logs")

fh = RotatingFileHandler('./logs/cold_wallet.log', mode='a', maxBytes=5*1024*1024, backupCount=2, encoding='utf8', delay=0)
fh.setFormatter(formatter)
logger.addHandler(fh)


class DatabaseUtil():
    """
    Database(MySQL) 접속 유틸
    """
    config = None
    cursor = None
    connection = None;

    def __init__(self, config):
        self.config = config

    def get_connection(self):
        """
        Database 접속 처리 메서드
        클래스 인스턴스 생성시 전달된 config 데이터를 기반으로 접속정보를 처리하고
        connection과 cursor를 반환한다.
        """
        host        = self.config.get('HOST', None)
        port        = int(self.config.get('PORT', None))
        user        = self.config.get('USER', None)
        password    = self.config.get('PASSWORD', None)
        db          = self.config.get('NAME', None)
        charset     = self.config.get('CHARSET', None)

        if host is None :
            raise Exception('Database host is not define.')
        
        if port is None :
            port = 3306
        
        if user is None :
            raise Exception('Database user is not define.')
        
        if password is None :
            raise Exception('Database password is not define.')
        
        if db is None :
            raise Exception('Database name is not define.')
        
        if charset is None :
            charset = 'utf8'

        self.connection = pymysql.connect(host=host, port=port, user=user, passwd=password, db=db, charset=charset)
        self.cursor = self.connection.cursor()

        return {'connection': self.connection, 'cursor': self.cursor}

    def close_db(self):
        """
        DB 커넥션을 종료한다.
        """
        self.cursor.close()
        self.connection.close()

class RedisUtil():
    """
    레디스 DB 접속유틸
    """
    config = None
    redis_connect = None

    def __init__(self, config):
        self.config = config


    def connect(self) :
        host        = self.config.get('HOST', None)
        port        = self.config.get('PORT', None)
        password    = self.config.get('PASSWORD', None)

        self.redis_connect = Redis(host=host, port=port, password=password)

        return self.redis_connect

    def close(self):
        self.redis_connect.connection_pool.disconnect()


class ColdWalletCollector():
    """
    Cold Wallet의 코인 수량을 수집해 Redis에 저장하는 클래스
    """
    SQL_SELECT_COLD_WALLET = "SELECT * FROM deposit_address WHERE wallet_type = 'COLD' ORDER BY currency ASC"
    REDIS_SET_LOCATION = 'bcg:coldwallet:balance'

    deposit_list = []
    currency_list = None

    def get_cold_wallet_list(self):
        """
        백오피스에서 등록된 Cold Wallet 주소를 찾아온다.
        """
        database = DatabaseUtil(config.DATABASE)
        connection_data = database.get_connection()
        cursor = connection_data['cursor']
        cursor.execute(self.SQL_SELECT_COLD_WALLET)

        self.deposit_list = []
        
        logger.debug("======== wallet list ========")
        
        for row in cursor:
            n = row.__len__();
            model = {}

            for i in range(n):
                model[cursor.description[i][0]] = row[i]
            logger.debug("ID : " + str(model['id']))
            logger.debug("CURRENCY : " + str(model['currency']))
            logger.debug("ADDRESS : " + model['address'])
            logger.debug("NICK : " + model['nick'])

            self.deposit_list.append(model)

        database.close_db()

    def get_currency_list(self):
        """
        코인 목록 가져오기
        """
        logger.debug("======== get currency list ========")
        result = requests.get(config.BACKOFFICE_BACKEND_HOST + config.CURRENCY_LIST_API)
        self.currency_list = result.json()
        for item in self.currency_list :
            logger.debug("ID : " + str(item['id']))
            logger.debug("CODE : " + item['code'])
            
        return self.currency_list

    def find_wallets(self, currency):
        """
        코인에 맞는 지갑목록을 찾아오기
        """
        wallet_list = []


        for item in self.deposit_list:
            if item['currency'] == currency:
                wallet_list.append(item)
        

        return wallet_list;

    def save_currency_coin(self):
        """
        Cold Wallet 코인을 Redis에 저장하는 메서드
        """
        currency_list = self.get_currency_list()

        redis = RedisUtil(config.REDIS)
        redis_connect = redis.connect()
        logger.debug("---------------------------------------------")
        logger.debug("Cold wallet collect balances start.")

        getBlanaceOutsideList = ['BTC', 'QTUM', 'BCH', 'ADA']

        for item in currency_list:
            coin_name = item['code'].upper()

            for wallet in self.find_wallets(item['id']) :
                if coin_name in getBlanaceOutsideList:
                    if config.IS_TESTNET :
                        api = config.TEST_NET_COIN_API[coin_name].format(wallet['address'])
                    else :
                        api = config.MAIN_NET_COIN_API[coin_name].format(wallet['address'])

                    if api is not None :
                        rs = requests.get(api)
                        data = rs.json()
                        balance = 0

                        if coin_name == 'BTC':
                            if 'final_balance' not in data.keys():
                                continue

                            balance = data['final_balance']
                            balance = float(balance) * 0.00000001

                        elif coin_name == 'BCH':
                            balance = float(data) * 0.00000001

                        elif coin_name == 'QTUM':
                            balance = float(data) * 0.00000001

                        elif coin_name == 'ADA':
                            balance = float(data['Right']['caBalance']['getCoin']) * 0.000001
                else:
                    manager = CoinManager()

                    if coin_name is None:
                        return Response(status=status.HTTP_400_BAD_REQUEST)

                    balance = float(manager.getCoinBlance(coin_name, wallet['address'])['result'])

                redis_connect.set(self.REDIS_SET_LOCATION + ":" + coin_name + ":" + wallet['address'], balance)
                
                logger.debug("---------------------------------------------")
                logger.debug(coin_name + " wallet recorded balance.")
                logger.debug("* Address : " + wallet['address'])
                logger.debug("* Balances : " + str(balance) )
                logger.debug("* Date : " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        redis.close()


class Scheduler:
    def __init__(self):
        self.sched = BackgroundScheduler()
        self.sched.start()
        self.job_id = ''

    def __del__(self):
        self.shutdown()

    def shutdown(self):
        self.sched.shutdown()

    def kill_scheduler(self, job_id):
        try:
            self.sched.remove_job(job_id)
        except JobLookupError as err:
            logger.debug("fail to stop Scheduler: {err}".format(err=err))
            return

    def get_cold_wallet_job(self, type, job_id):
        logger.debug("%s Scheduler process_id[%s] : %d" % (type, job_id, time.localtime().tm_sec))
        collector = ColdWalletCollector()
        collector.get_cold_wallet_list()
        collector.save_currency_coin()

    def scheduler(self, type, job_id):
        logger.debug("{type} Scheduler Start".format(type=type))
        self.sched.add_job(self.get_cold_wallet_job, type, seconds=config.BALANCE_COLLECT_PERIOD, id=job_id, args=(type, job_id))

if __name__ == '__main__':

    while True:
        scheduler = Scheduler()
        scheduler.scheduler('interval', "1")

        if config.SCHEDULER_START_NOW :
            scheduler.get_cold_wallet_job('interval', '1')
        time.sleep(config.BALANCE_COLLECT_PERIOD)
