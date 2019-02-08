from pymongo import MongoClient
from bson.objectid import ObjectId
from config import mongodb

class Mongodb:
    def __init__(self, host=mongodb['host'], port=mongodb['port'], db=mongodb['db']):
        self.host = host
        self.port = port
        self.client = MongoClient(host, port)
        self.db = self.client[db]

    def get_collection(self, collection):
        return self.db[collection]

    def insert(self, collection, documents):
        # document keys validation
        ids = self.db[collection].insert(documents)
        return ids

    def delete(self, collection, document):
        return self.db[collection].delete_one(document)

    def delete_all(self, collection, confirmation=False):
        if confirmation:
            return self.db[collection].delete_many({})
        else:
            print('error noop. confirmation is set to false')
            return None

    def find(self, collection, document):
        return self.db[collection].find(document)

    def increment(self, collection, document, id=False):
        if id:
            return self.db[collection].update( { '_id': ObjectId(document) }, { '$inc': { 'n': 1 } } )
        else:
            print('increment not using id')
            return self.db[collection].update_many( document, { '$inc' : { 'n': 1 } } )
