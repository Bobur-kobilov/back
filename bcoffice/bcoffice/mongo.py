from django.conf import settings
from bson.codec_options import CodecOptions
import pymongo
import pytz


class BCOfficeMongoDB:
    def __init__(self, __setting_name__ = 'default', collection = None):
        if collection is not None :
            self.mongo_connect(__setting_name__, collection)
        else :
            self.db_client = None
            self.db_name = None

            self.__setting_name__ = __setting_name__
            self.collection = collection

    __setting_name__ = None

    db_client = None
    db_name = None
    db = None
    collection = None
    
    # 몽고DB 연결
    def mongo_connect(self, __setting_name__='default', collection = None):
        db_settings = settings.MONGODB_DATABASES[__setting_name__]
        self.db_name = db_settings.get('NAME', None)
        host = db_settings.get('HOST', None)
        port = db_settings.get('PORT', None)
        user = db_settings.get('USER', None)
        password = db_settings.get('PASSWORD', None)

        if user is not None and password is not None :
            addr = 'mongodb://%s:%s@%s:%s' % (user, password, host, port)
            self.db_client = pymongo.MongoClient(addr)
        else :
            self.db_client = pymongo.MongoClient(host=host, port=port)

        self.db = self.db_client[self.db_name]

        if collection is not None :
            self.collection = self.db[collection]
            self.collection.with_options(
                codec_options=CodecOptions(
                    tz_aware=True
                    , tzinfo=pytz.timezone('Asia/Seoul')
                )
            )

    def insert_db(self, data=None):
        self.collection.insert({'body':data})

    def update_db(self, key=None, key_value=None, update_data=None):
        self.collection.update({key:key_value}, {'body': update_data}, upsert=True)

    def remove_db(self, key=None, key_value=None, init=False):
        if init: # 컬렉션 초기화
            self.collection.remove()
        else:
            self.collection.remove({key:key_value})

    def get_db_client(self):
        return self.db_client

    def get_db(self):
        return self.db

    # 몽고 DB 연결 해제
    def close(self):
        self.db_client.close()