from pymongo import MongoClient
from bson.objectid import ObjectId
from config import mongodb, active_rate
import gridfs
import datetime


class Mongodb:
    def __init__(self, host=mongodb['host'], port=mongodb['port'], db=mongodb['db']):
        self.host = host
        self.port = port
        self.client = MongoClient(host, port)
        self.db = self.client[db]
        self.fs = gridfs.GridFS(self.db)

    # gets the object referenced by _id
    def getObjectIdDocument(self, _id):
        return {'_id': ObjectId(_id)}

    # gets pointer to a collection
    def get_collection(self, collection, db=None):
        coll = self.client[db][collection] if db else self.db[collection]
        return coll

    # gets all documents saved in a collection
    def get_all(self, collection, db=None):
        cursor = self.get_collection(collection).find()
        return list(cursor)

    # gets the member by id
    def get_member(self, id):
        return list(self.find('members', id))[0]

    # gets the image in grid fs by id
    def get_image(self, id):
        return self.fs.get(id).read()

    # inserts documents into a collection
    def insert(self, collection, documents, db=None):
        # TODO: document keys validation
        coll = self.client[db][collection] if db else self.db[collection]
        ids = coll.insert(documents)
        return ids

    # deletes documents in a collection
    def delete(self, collection, document, db=None):
        coll = self.client[db][collection] if db else self.db[collection]
        if type(document) == str or type(document) == ObjectId:
            return coll.delete_many(self.getObjectIdDocument(document))
        else:
            return coll.delete_many(document)

    # deletes all documents in a collection
    def delete_all(self, collection, confirmation=False, db=None):
        if confirmation:
            return self.delete(collection, {}, db)
        else:
            print('ERROR: confirmation is set to false')
            return None

    # finds a document in a collection by id or by the whole document
    def find(self, collection, document={}, db=None):
        coll = self.client[db][collection] if db else self.db[collection]
        if type(document) == str or type(document) == ObjectId:
            return coll.find(self.getObjectIdDocument(document))
        else:
            return coll.find(document)

    # increments the number in a collection
    def increment(self, collection, document, db=None):
        coll = self.client[db][collection] if db else self.db[collection]
        if type(document) == str or type(document) == ObjectId:
            return coll.update(self.getObjectIdDocument(document), {'$inc': {'n': 1}})
        else:
            return coll.update_many(document, {'$inc': {'n': 1}})

    def init_calendar(self, id, name, year):
        document = {
            'member_id': id,
            'member_name': name,
            'year': year,
            'days': {}
        }
        return self.init_calendar(document)

    def init_calendar(self, document):
        collection = self.get_collection('calendar')
        return collection.insert_one(document)

    def find_calendar_by_id(self, id):
        collection = self.get_collection('calendar')
        return collection.find_one(id)

    def find_calendar_document_by_year(self, year):
        collection = self.get_collection('calendar')
        return collection.find_one({{ 'year': year}})

    def get_total_from_document(self, document):
        return self.get_total(document['year']['days'])

    def get_count_from_document(self, document):
        return self.get_count(document['year']['days'])

    def get_total(self, days):
        return len(days)

    def get_count(self, days):
        count = 0
        for day in days:
            if days[day] == True:
                count += 1
        return count

    def is_active_by_document(self, document, rate=active_rate):
        total = self.get_total(document)
        count = self.get_count(document)
        return True if count / total >= rate else False

    # if event occurs
    def event_occured(self, timestamp, member_id, member_name):
        coll = self.get_collection('calendar')
        dt = datetime.datetime.fromtimestamp(timestamp).replace(microsecond=0)
        # if dt.weekday() == 6: # sunday
        key = dt.isoformat()
        document = coll.find_one({
            'member_id': self.getObjectIdDocument(member_id),
            'member_name': member_name,
        })

        document['days'][key] = True
        return coll.update({ '_id': document['_id'] },
                { '$set': { 'days': document['days'] } }, upsert=True) # add day
