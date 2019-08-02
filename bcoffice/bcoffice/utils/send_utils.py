import json

# from becoin.model                   import Members

from bcoffice.queue                 import (
    QueueUtil
    , SMS_KEY
    , SMS_ROUTING_KEY
    , EMAIL_KEY
    , EMAIL_ROUTING_KEY
    , EXCHANGE_NOTIFICATION
    , TBL_BCOFFICE_SEND_MAIL_HISTORY
    , TBL_BCOFFICE_SEND_SMS_HISTORY
)

from datetime                       import datetime
from bcoffice.utils import logging_utils

class SendMail:
    # 메일전송 및 Log 남기는 기능
    # sender_id         : 작성자
    # target_list       : 리스트 형식의 수신자
    # title, contents   : 제목, 내용
    def send(sender_id = None, target_list = None, title = None, contents = None):
        # 리스트 None값 제거
        target_list = list(filter(None, target_list))

        # 리스트 중복제거
        target_list = list(set(target_list))

        queue = QueueUtil()

        # 메일보내기 (MQ 전송)
        queue.open(key=EMAIL_KEY)
        
        # mailer_class: 'BackofficeMailer', method: 'test', args: ['setia@naver.com', 'contentes...']
        for target in target_list:
            info = {}
            info['mailer_class'] = 'BackofficeMailer'
            info['method'] = 'notice'
            info['args'] = [target, title, contents]

            s = json.dumps(info)

            queue.publish(body=s, routing_key=EMAIL_ROUTING_KEY, exchange=EXCHANGE_NOTIFICATION)

        queue.close()

class SendSMS:
    # SMS전송 및 Log 남기는 기능
    # sender_id         : 작성자
    # target_list       : 리스트 형식의 수신자
    # message           : 내용
    def send(sender_id = None, target_list = None, message = None):
        # 리스트 None값 제거
        target_list = list(filter(None, target_list))

        # 리스트 중복제거
        target_list = list(set(target_list))

        queue = QueueUtil()

        # SMS 보내기 (MQ 전송)
        queue.open(key=SMS_KEY)
        
        for target in target_list:
            info = {}
            info['phone'] = target
            info['message'] = message

            s = json.dumps(info)

            queue.publish(body=s, routing_key=SMS_ROUTING_KEY, exchange=EXCHANGE_NOTIFICATION)

        queue.close()