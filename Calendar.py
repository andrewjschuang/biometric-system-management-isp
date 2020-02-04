from datetime import datetime
from Presence import Presence
from Sunday import Sunday
from config import active_rate


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
