from bcoffice.queue import (
    QueueUtil
    , WITHDRAW_COIN
)
import json

def request_withdraw(withdraw_id):
    queue = QueueUtil()
    queue.open(WITHDRAW_COIN, durable=False)

    val = {'id': withdraw_id }
    jsonval = json.dumps(val)
    queue.publish(
        body=jsonval
        , routing_key=WITHDRAW_COIN
        , exchange='')

    queue.close()