from bcoffice.queue import (
    QueueUtil
    , CENTRAL_LOGGING
)

def set_log(table_name = None, body = None):
    queue = QueueUtil()
    queue.open( CENTRAL_LOGGING )
        
    queue.publish(
        body=body
        , headers={'tblname': table_name}
        , routing_key=CENTRAL_LOGGING
        , exchange='')

    queue.close()
