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

    def replace_member(self, _id, member):
        return self._replace(_id, member.to_dict())

    def delete_member(self, _id):
        return self._delete_by_id(_id)

    def find_members_by_date(self, date):
        return list(self.collection.find({
            "calendar": {
                "$elemMatch": {
                    "$expr": {
                        "$in": [
                            date,
                            {
                                "$map": {
                                    "input": {"$objectToArray": "$$this"},
                                    "as": "entry",
                                    "in": {
                                        "$dateToString": {
                                            "format": "%Y-%m-%d",
                                            "date": {"$toDate": {"$toLong": "$$entry.k"}}
                                        }
                                    }
                                }
                            }
                        ]
                    }
                }
            }
        }))

    def add_presence(self, _id, ts, photo_id):
        result = self.collection.update_one(
            self._object_id(_id),
            {"$addToSet": {"calendar": {str(ts): photo_id}}}
        )
        return result.modified_count > 0

    def remove_presence(self, _id, ts):
        result = self.collection.update_one(
            self._object_id(_id),
            {"$pull": {"calendar": {str(ts): {"$exists": True}}}}
        )
        return result.modified_count > 0
