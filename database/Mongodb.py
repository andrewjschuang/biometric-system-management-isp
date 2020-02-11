import datetime
from pymongo import MongoClient
from gridfs import GridFS
from bson.objectid import ObjectId
from config import mongodb, active_rate
import database.sundays as sundays


class Mongodb:
    def __init__(self, host=mongodb['host'], port=mongodb['port'], db=mongodb['db']):
        self.host = host
        self.port = port
        self.client = MongoClient(host, port)
        self.db = self.client[db]
        self.fs = GridFS(self.db)

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
        members = self.find('members', id)
        return list(members)[0]

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

    def update(self, collection, id, field, document, operator, upsert=True):
        return collection.update({'_id': id},
                                 {operator: {field: document}}, upsert)

    # calendar operations

    def init_calendar(self, member, force=False):
        collection = self.get_collection('members')
        year = str(datetime.datetime.now().year)
        if 'calendar' not in member:
            member['calendar'] = {}
        if force or (year not in member['calendar']):
            member['calendar'][year] = {}
            for day in sundays.get_sundays_from_year(int(year)):
                member['calendar'][year][day] = 'Ausente'
        self.update(collection, member['_id'], 'calendar', member['calendar'], '$set')
        return member['calendar']

    def update_calendar(self, member, document):
        collection = self.get_collection('members')
        return self.update(collection, member['_id'], 'calendar', document, '$set')

    def get_total(self, days):
        return len(days)

    def get_count(self, days):
        count = 0
        for day in days:
            if days[day] == 'Presente':
                count += 1
        return count

    def is_active_by_document(self, document, rate=active_rate):
        total = self.get_total(document)
        if total <= 0:
            return False
        count = self.get_count(document)
        return True if count / total >= rate else False

    # if event occurs
    def event_occured(self, timestamp, member_id, member_name):
        collection = self.get_collection('members')
        dt = datetime.datetime.fromtimestamp(timestamp).replace(microsecond=0)
        if sundays.is_sunday(dt):
            key = '%s-%s' % (dt.month, dt.day)
            year = str(dt.year)
            member = self.get_member(member_id)
            if 'calendar' not in member:
                member['calendar'] = self.init_calendar(member)
            if year not in member['calendar']:
                member['calendar'][year] = { key: 'Presente' }
            else:
                member['calendar'][year][key] = 'Presente'
            self.update_calendar(member, member['calendar'])
