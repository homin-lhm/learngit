# coding=utf8
import pymongo
import os
import datetime


# ======== mongoDB base operating ===================
class mongoDB(object):

    def __init__(self, kw):
        self.connection = pymongo.MongoClient(kw["host"], int(kw["port"]))
        self.db = self.connection[kw["db"]]

    # clear table data
    def clear(self, table_name):
        collection = self.db[table_name]
        collection.remove()

    # insert sql statement
    def insert_data(self, table_name, table_data):
        collection = self.db[table_name]
        collection.insert_many(table_data)

    # close database
    def close(self):
        self.connection.close()

    def init_data(self, datas):
        for table, data in datas.items():
            self.clear(table)
            self.insert_data(table, data)
        self.close()


if __name__ == '__main__':
    datas = {
        "click_cache": [
            {
                "affiliateId": 2,
                "createTime": datetime.datetime.strptime('2018-06-12', '%Y-%m-%d'),
                "offerId": 2,
                "subAffId": "subAffId1",
                "value": 5000
            }
        ],
        "conversion_cache": [
            {
                "affiliateId": 2,
                "createTime": datetime.datetime.strptime('2018-06-12', '%Y-%m-%d'),
                "offerId": 2,
                "subAffId": "subAffId1",
                "value": 5000
            }
        ]
    }
    mongoDB().init_data(datas)
