from database.MongoConnector import MongoConnector
from entities.Person import Person


class MembersCollection(MongoConnector):
    def __init__(self):
        super().__init__()
        super()._set_collection('members')

    # gets all members and initializes to a list of Persons
    def get_all_members(self):
        documents = self._get_all_documents()
        return [Person.from_dict(member) for member in documents]

    # gets the member by id
    def get_member_by_id(self, _id):
        member = self._find_by_id(_id)
        return Person.from_dict(member)

    def insert_member(self, member):
        return self._insert(member.to_dict())

    def update_member_calendar(self, member):
        pass
        # return self._update(member._id, 'calendar', member.calendar, '$set', upsert=True)

    def replace_member(self, member_id, member):
        return self._replace(member_id, member.to_dict())

    def delete_member(self, _id):
        return self._delete_by_id(_id)
