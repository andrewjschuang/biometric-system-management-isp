from database.MongoConnector import MongoConnector
from entities.Person import Person


class MembersCollection(MongoConnector):
    def __init__(self):
        super().__init__()
        self.__set_collection('members')

    # gets all members and initializes to a list of Persons
    def get_all_members(self):
        documents = self.__get_all_documents()
        return [Person.from_dict(member).set_id(member['_id']) for member in documents]

    # gets the member by id
    def get_member_by_id(self, _id):
        member = self.__find_by_id(_id).next()
        return Person.from_dict(member).set_id(member['_id'])

    def insert_member(self, member):
        return self.__insert(member)

    def update_member_calendar(self, member):
        return self.__update(member._id, 'calendar', member.calendar, '$set', upsert=True)

    def replace_member(self, member_id, member):
        return self.collection.replace_one(member_id, member)

    def delete_member(self, _id):
        return self.__delete_by_id(_id)
