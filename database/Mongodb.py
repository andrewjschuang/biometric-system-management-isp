import datetime
from pymongo import MongoClient
from gridfs import GridFS
from bson.objectid import ObjectId
from config import mongodb, active_rate


from entities.Sunday import Sunday
from entities.Collections import Collections
from entities.Person import Person


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
    def __get_collection(self, collection, db=None):
        return self.client[db][collection] if db else self.db[collection]

    # gets all documents saved in a collection
    def get_all_documents_in_collection(self, collection_name, db=None):
        return list(self.__get_collection(collection_name, db).find())

    # gets all members and initializes to a list of Persons
    def get_all_members(self):
        return [initialize_person(x) for x in self.get_all_documents_in_collection(Collections.MEMBERS.name)]

    # gets the member by id
    def get_member_by_id(self, _id):
        return initialize_person(self.find(Collections.MEMBERS.name, _id).next())

    # gets the image in grid fs by id
    def get_image(self, _id):
        return self.fs.get(_id).read()

    # inserts documents into a collection
    def insert(self, collection_name, documents, db=None):
        # TODO: document keys validation
        collection = self.__get_collection(collection_name, db)
        return collection.insert(documents)

    # deletes documents in a collection
    def delete(self, collection_name, document, db=None):
        collection = self.__get_collection(collection_name, db)
        if type(document) == str or type(document) == ObjectId:
            return collection.delete_many(self.getObjectIdDocument(document))
        else:
            return collection.delete_many(document)

    # deletes all documents in a collection
    def delete_all(self, collection_name, confirmation=False, db=None):
        if confirmation:
            collection = self.__get_collection(collection_name, db)
            return self.delete(collection, {}, db)
        else:
            print('ERROR: confirmation is set to false')
            return None

    # finds a document in a collection by id or by the whole document
    def find(self, collection_name, document={}, db=None):
        collection = self.__get_collection(collection_name, db)
        if type(document) == str or type(document) == ObjectId:
            return collection.find(self.getObjectIdDocument(document))
        else:
            return collection.find(document)

    def __update(self, collection_name, _id, field, document, operator, upsert=True):
        collection = self.__get_collection(collection_name)
        return collection.update({'_id': _id}, {operator: {field: document}}, upsert)

    # calendar operations

    def update_member_calendar(self, member):
        return self.__update(Collections.MEMBERS.name, member._id, 'calendar', member.calendar.to_dict(), '$set')

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
        if Sunday.is_sunday(dt):
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

def initialize_person(person):
    return Person.from_dict(person).set_id(person['_id'])
