from django.conf import settings

import pika

CENTRAL_LOGGING                 = 'bcg.central_logging'

WITHDRAW_COIN                 = 'bcg.withdraw.coin'

SMS_KEY = 'sms'
EMAIL_KEY = 'email'

EXCHANGE_NOTIFICATION = 'bcg.notification'

SMS_ROUTING_KEY = 'bcg.notification.sms'

EMAIL_ROUTING_KEY = 'bcg.notification.email'

# 회원정정 테이블
TBL_BCOFFICE_MEMBER_MOD         = 'bcoffice_member_modifies'

# 회원 추천인 수수료 정정 테이블
TBL_BCOFFICE_REFERRAL_FEE_MOD   = 'bcoffice_referral_fee_modifies'

# 회원 추천인 수수료 정정 테이블
TBL_BCOFFICE_REFERRAL_COMMISSION_MOD   = 'bcoffice_referral_commission_modifies'

# 보안등급(입출금) 정책 조회 테이블
TBL_BCOFFICE_DEPOSIT_WITHDRAW_MOD   = 'bcoffice_deposit_withdraw_modifies'

# 메일 발송내역 테이블
TBL_BCOFFICE_SEND_MAIL_HISTORY  = 'bcoffice_send_mail_histories'

# SMS 발송내역 테이블
TBL_BCOFFICE_SEND_SMS_HISTORY  = 'bcoffice_send_sms_histories'

# SMS 발송내역 테이블
TBL_BCOFFICE_MTS_VERSION_HISTORY  = 'bcoffice_mts_version_histories'

# 블랙리스트 테이블
TBL_BCOFFICE_BLACKLIST  = 'bcoffice_blacklist'

# 블랙리스트 출금요청 내역 테이블
TBL_BCOFFICE_BLACKLIST_WITHDRAW_PROC  = 'bcoffice_blacklist_withdraw_proc'

# 회원 코인수량 정정 테이블
TBL_BCOFFICE_MODIFY_COIN_AMOUNT = 'bcoffice_modify_coin_amount'

# 거래내역 강제취소 테이블
TBL_BCOFFICE_ORDER_FORCE_CANCEL = 'bcoffice_order_force_cancel'

# 거래 승인 내역 컬렉션
TBL_BCOFFICE_WITHDRAW_CONFIRM = 'bcoffice_withdraw_confirm'

# 수동출금처리 취소
TBL_BCOFFICE_WITHDRAW_CANCEL = 'bcoffice_withdraw_cancel'

# 고객입출금 합계
TBL_BCOFFICE_DAILY_DEPOSIT_WITHDRAW = 'bcoffice_daily_deposit_withdraw'

# 일별 매출액
TBL_BCOFFICE_DAILY_TOTAL_SALES = 'bcoffice_daily_total_sales'

# 코인별 거래현황
TBL_BCOFFICE_COIN_TRANSACTION_STATUS = 'bcoffice_coin_transaction_status'

# 고객 지원 내역
TBL_BCOFFICE_SUPPORT_HISTORY = 'bcoffice_support_history'

# 거래운영
TBL_BCOFFICE_TRADE_OPERATIONS = 'bcoffice_trade_operations'

# 레퍼럴 현황
TBL_BCOFFICE_REFERRAL_STATUS = 'bcoffice_referral_status'

TBL_BCOFFICE_BLACKLIST_IP = "bcoffice_blacklist_ip"

class QueueUtil :
    connection = None
    channel = None

    def open(self, key, durable=True):
        self.connection = pika.BlockingConnection( pika.ConnectionParameters(
            host = settings.RABBIT_MQ['URL']
            , port = settings.RABBIT_MQ['PORT']
            , credentials= pika.PlainCredentials( 
                settings.RABBIT_MQ['USER']
                , settings.RABBIT_MQ['PASSWORD']
            )
        ))

        self.set_channel(key, durable)

    def set_channel(self, key, durable=True):
        self.channel = self.connection.channel()
        # https://github.com/ShoppinPal/intranet-router-node/issues/2
        # http://rubybunny.info/articles/queues.html
        self.channel.queue_declare(queue=key, durable=durable)
        # self.channel.queue_declare(queue=key)

    def publish(self, body, headers=None, routing_key='', exchange=''):
        # {'tblname': table_name}
        self.channel.basic_publish(
            exchange=exchange
            , properties=pika.BasicProperties(
                headers=headers
            )
            , routing_key=routing_key
            , body = body
        )

    def close(self):
        self.connection.close()
