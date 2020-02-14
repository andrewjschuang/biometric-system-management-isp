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
    def __get_object_id_document(self, _id):
        return {'_id': ObjectId(_id)}

    # gets pointer to a collection
    def __get_collection(self, collection, db=None):
        return self.client[db][collection] if db else self.db[collection]

    # gets all documents saved in a collection
    def __get_all_documents_in_collection(self, collection_name):
        return list(self.__get_collection(collection_name).find())

    # inserts documents into a collection
    def __insert(self, collection_name, documents, db=None):
        # TODO: document keys validation
        collection = self.__get_collection(collection_name, db)
        return collection.insert(documents)

    def __update(self, collection_name, _id, field, document, operator, upsert=True):
        collection = self.__get_collection(collection_name)
        return collection.update({'_id': _id}, {operator: {field: document}}, upsert)

    # deletes all documents in a collection
    def __delete_all(self, collection_name):
        collection = self.__get_collection(collection_name)
        return self.__delete(collection, {})

    # deletes documents in a collection
    def __delete(self, collection_name, document):
        collection = self.__get_collection(collection_name)
        if type(document) == str or type(document) == ObjectId:
            return collection.delete_many(self.__get_object_id_document(document))
        else:
            return collection.delete_many(document)

    # finds a document in a collection by id or by the whole document
    def __find(self, collection_name, document={}):
        collection = self.__get_collection(collection_name)
        if type(document) == str or type(document) == ObjectId:
            return collection.find(self.__get_object_id_document(document))
        else:
            return collection.find(document)

    ''' ---------- MEMBERS METHODS ---------- '''

    # gets all members and initializes to a list of Persons
    def get_all_members(self):
        return [initialize_person(x) for x in self.__get_all_documents_in_collection(Collections.MEMBERS.name)]

    # gets the member by id
    def get_member_by_id(self, _id):
        return initialize_person(self.__find(Collections.MEMBERS.name, _id).next())

    def insert_member(self, member):
        member.update_active()
        self.__insert(Collections.MEMBERS.name, member.to_dict())

    def update_member_calendar(self, member):
        member.update_active()
        return self.__update(Collections.MEMBERS.name, member._id, 'calendar', member.calendar.to_dict(), '$set')

    def replace_member(self, member_id, person):
        collection = self.__get_collection(Collections.MEMBERS.name)
        return collection.replace_one(__get_object_id_document(member_id), person.to_dict())

    def delete_member(self, _id):
        return self.delete(Collections.MEMBERS.name, ObjectId(_id))

    # deletes all documents in a collection
    def delete_all_members(self, confirmation=False):
        if confirmation:
            return self.__delete_all(Collections.MEMBERS.name)
        else:
            print('ERROR: confirmation is set to false')
            return None

    ''' ---------- ENCODINGS METHODS ---------- '''

    def get_all_encodings(self):
        encodings = self.__find(Collections.ENCODINGS.name, {})
        return [Encoding.from_dict(encoding) for encoding in encodings]

    def insert_encoding(self, encoding):
        self.__insert(Collections.ENCODINGS.name, encoding.to_dict())

    def delete_encoding(self, _id):
        return self.delete(Collections.ENCODINGS.name, ObjectId(_id))

    # deletes all documents in a collection
    def delete_all_encodings(self, confirmation=False):
        if confirmation:
            return self.__delete_all(Collections.ENCODINGS.name)
        else:
            print('ERROR: confirmation is set to false')
            return None

    ''' ---------- EVENTS METHODS ---------- '''

    def insert_event(self, event):
        self.__insert(Collections.EVENTS.name, event.to_dict())

    ''' ---------- IMAGES METHODS ---------- '''

    # gets the image in grid fs by id
    def get_image(self, _id):
        return self.fs.get(_id).read()
