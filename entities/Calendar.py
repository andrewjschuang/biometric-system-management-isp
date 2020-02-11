from datetime import datetime
from config import active_rate
from entities.Presence import Presence
from entities.Sunday import Sunday


class Calendar:

    def __init__(self, sundays=None, year=datetime.now().year):
        self.sundays = sundays if sundays is not None else Sunday.get_sundays_from_year(
            year)
        self.active = False if sundays is None else is_active()

    def is_active(self):
        size = len(self.sundays)
        if size == 0:
            return False
        return True if self.presence_count() / size >= active_rate else False

    def presence_count(self):
        count = 0
        for day in self.sundays:
            if day == Presence.Present:
                count += 1
        return count

    def to_dict(self):
        return {
            'sundays': [x.to_dict() for x in self.sundays],
            'active': self.active
        }
