from django.conf import settings
from bson.codec_options import CodecOptions
import pymongo
import pytz

class BCOfficeBlackListMongoDB:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(BCOfficeBlackListMongoDB, cls).__new__(cls)
            cls._instance.mongo_connect(collection=kwargs['collection'])
        else:
            cls._instance.connect_collection(collection=kwargs['collection'])
        return cls._instance

    __setting_name__ = None

    db_client = None
    db_name = None
    db = None
    collection = None
    
    # 몽고DB 연결
    def mongo_connect(self, __setting_name__='blacklist', collection = None):
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
        self.connect_collection(collection)

    def connect_collection(self, collection):
        if collection is not None:
            self.collection = self.db[collection]
            self.collection.with_options(
                codec_options=CodecOptions(
                    tz_aware=True
                    , tzinfo=pytz.timezone('Asia/Seoul')
                )
            )

    def get_db_client(self):
        return self.db_client

    def get_db(self):
        return self.db

    # 몽고 DB 연결 해제
    def close(self):
        self.db_client.close()