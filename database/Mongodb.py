import datetime
from pymongo import MongoClient
from gridfs import GridFS
from bson.objectid import ObjectId
from config import mongodb, active_rate

from entities.Sunday import Sunday
from entities.Collections import Collections
from entities.Person import Person
from entities.Encoding import Encoding

def initialize_person(person):
    return Person.from_dict(person).set_id(person['_id'])

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

    def __update(self, collection_name, _id, field, document, operator, upsert=True):
        collection = self.__get_collection(collection_name)
        return collection.update({'_id': _id}, {operator: {field: document}}, upsert)

    # gets all documents saved in a collection
    def get_all_documents_in_collection(self, collection_name, db=None):
        return list(self.__get_collection(collection_name, db).find())

    # gets all members and initializes to a list of Persons
    def get_all_members(self):
        return [initialize_person(x) for x in self.get_all_documents_in_collection(Collections.MEMBERS.name)]

    # gets the member by id
    def get_member_by_id(self, _id):
        return initialize_person(self.find(Collections.MEMBERS.name, _id).next())

    def delete_member(self, _id):
        return self.delete(Collections.MEMBERS.name, ObjectId(_id))

    def delete_encoding(self, _id):
        return self.delete(Collections.ENCODINGS.name, ObjectId(_id))

    def get_all_encodings(self):
        encodings = self.find(Collections.ENCODINGS.name, {})
        return [Encoding.from_dict(encoding) for encoding in encodings]

    # gets the image in grid fs by id
    def get_image(self, _id):
        return self.fs.get(_id).read()

    # inserts documents into a collection
    def insert(self, collection_name, documents, db=None):
        # TODO: document keys validation
        collection = self.__get_collection(collection_name, db)
        return collection.insert(documents)

    def insert_member(self, member):
        member.update_active()
        self.insert(Collections.MEMBERS.name, member.to_dict())

    def update_member_calendar(self, member):
        member.update_active()
        return self.__update(Collections.MEMBERS.name, member._id, 'calendar', member.calendar.to_dict(), '$set')

    def replace_member(self, collection_name, member_id, person):
        collection = self.__get_collection(collection_name)
        return collection.replace_one({'_id': member_id}, person)

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
