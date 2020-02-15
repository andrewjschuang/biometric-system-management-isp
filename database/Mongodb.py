import datetime
from pymongo import MongoClient
from gridfs import GridFS
from bson.objectid import ObjectId
from config import mongodb, active_rate

from entities.Sunday import Sunday
from entities.Collections import Collections
from entities.Person import Person
from entities.Encoding import Encoding

def initialize_member(member):
    return Person.from_dict(member).set_id(member['_id'])

class Mongodb:
    def __init__(self, host=mongodb['host'], port=mongodb['port'], db=mongodb['db']):
        client = MongoClient(host, port)
        db = client[db]
        fs = GridFS(db)
        self.client = client
        self.db = db
        self.fs = fs

    # gets the object referenced by _id
    def __get_object_id_document(self, _id):
        return {'_id': ObjectId(_id)}

    # gets pointer to a collection
    def __get_collection(self, collection):
        return self.db[collection]

    # gets all documents saved in a collection
    def __get_all_documents_in_collection(self, collection_name):
        return list(self.__get_collection(collection_name).find())

    # inserts documents into a collection
    def __insert(self, collection_name, documents):
        # TODO: document keys validation
        collection = self.__get_collection(collection_name)
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
        return collection.delete_many(document)

    # finds a document in a collection by id or by the whole document
    def __find(self, collection_name, document={}):
        collection = self.__get_collection(collection_name)
        if type(document) == str or type(document) == ObjectId:
            return collection.find(self.__get_object_id_document(document))
        return collection.find(document)

    ''' ---------- MEMBERS METHODS ---------- '''

    # gets all members and initializes to a list of Persons
    def get_all_members(self):
        return [initialize_member(x) for x in self.__get_all_documents_in_collection(Collections.MEMBERS.name)]

    # gets the member by id
    def get_member_by_id(self, _id):
        return initialize_member(self.__find(Collections.MEMBERS.name, _id).next())

    def insert_member(self, member):
        return self.__insert(Collections.MEMBERS.name, member.to_dict())

    def update_member_calendar(self, member):
        return self.__update(Collections.MEMBERS.name, member._id, 'calendar', member.calendar.to_dict(), '$set')

    def replace_member(self, member_id, member):
        collection = self.__get_collection(Collections.MEMBERS.name)
        return collection.replace_one(self.__get_object_id_document(member_id), member.to_dict())

    def delete_member(self, _id):
        return self.__delete(Collections.MEMBERS.name, ObjectId(_id))

    # deletes all documents in a collection
    def delete_all_members(self, confirmation=False):
        if confirmation:
            return self.__delete_all(Collections.MEMBERS.name)
        print('ERROR: confirmation is set to false')
        return None

    ''' ---------- ENCODINGS METHODS ---------- '''

    def get_all_encodings(self):
        encodings = self.__find(Collections.ENCODINGS.name, {})
        return [Encoding.from_dict(encoding) for encoding in encodings]

    def insert_encoding(self, encoding):
        return self.__insert(Collections.ENCODINGS.name, encoding.to_dict())

    def delete_encoding(self, _id):
        return self.__delete(Collections.ENCODINGS.name, ObjectId(_id))

    # deletes all documents in a collection
    def delete_all_encodings(self, confirmation=False):
        if confirmation:
            return self.__delete_all(Collections.ENCODINGS.name)
        print('ERROR: confirmation is set to false')
        return None

    ''' ---------- EVENTS METHODS ---------- '''

    def insert_event(self, event):
        return self.__insert(Collections.EVENTS.name, event.to_dict())

    ''' ---------- IMAGES METHODS ---------- '''

    # gets the image in grid fs by id
    def get_image(self, _id):
        return self.fs.get(_id).read()

    def insert_image(self, image):
        return self.fs.put(image)
