from database.MongoConnector import MongoConnector


class EventsCollection(MongoConnector):
    def __init__(self):
        super().__init__()
        super()._set_collection('events')

    def insert_event(self, event):
        return self._insert(event)
