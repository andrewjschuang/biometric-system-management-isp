from database.MongoConnector import MongoConnector


class EventsCollection(MongoConnector):
    def __init__(self):
        super().__init__()
        self.__set_collection('events')

    def insert_event(self, event):
        return self.__insert(event)
