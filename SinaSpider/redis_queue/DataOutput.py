from pymongo import MongoClient
from setting import *


class DataOutput(object):
    def __init__(self):
        self.conn = MongoClient('mongodb://127.0.0.1:27017', connect=False)
        self.coll = self.conn[DATABASE_NAME]
        self.db = self.coll[TABLE_NAME]
    def output_mongo(self, data):
        try:
            self.db.insert(dict(data))
        except Exception as e:
            logger.debug('data error:',e)

data = DataOutput()