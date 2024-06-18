from database.MongoConnector import MongoConnector
from datetime import datetime
from entities.Event import Event


class EventsCollection(MongoConnector):
    def __init__(self):
        super().__init__()
        super()._set_collection('events')

    def insert_event(self, event):
        return self._insert(event)

    def get_events_by_date(self, start_range=None, end_range=None, confirmed=None):
        today = datetime.now().date()
        if start_range is None:
            start_range = int(datetime.combine(
                today, datetime.min.time()).timestamp())
        if end_range is None:
            end_range = int(datetime.combine(
                today, datetime.max.time()).timestamp())

        query = {
            "timestamp": {
                "$gt": start_range,
                "$lt": end_range,
            }
        }

        if confirmed is not None:
            query["confirmed"] = confirmed

        documents = self._find(query, {"encoding": 0})
        return [Event.from_dict(event) for event in documents]
