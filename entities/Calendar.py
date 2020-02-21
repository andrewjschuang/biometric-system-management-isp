from datetime import datetime
from config import active_rate
from entities.Presence import Presence
from entities.Sunday import Sunday
from entities.Day import Day

class Calendar:
    def __init__(self, sundays=None, year=datetime.now().year):
        self.sundays = sundays if sundays is not None else Sunday.get_sundays_from_year(year)

    # TODO: change how sunday is found
    def mark_presence(self, day, presence):
        if not Sunday.is_sunday(day):
            return False
        for sunday in self.sundays:
            if sunday == day:
                sunday.presence = presence
                return True
        return False

    def is_active(self):
        count = 0
        total = 0
        today = Day.today()
        for sunday in self.sundays:
            if sunday > today:
                break
            if sunday.presence == Presence.PRESENT or sunday.presence == Presence.JUSTIFIED:
                count += 1
            total += 1
        return True if count / total >= active_rate else False

    def to_dict(self):
        return {
            'sundays': [x.to_dict() for x in self.sundays]
        }

    @staticmethod
    def from_dict(calendar):
        return Calendar([Sunday.from_dict(x) for x in calendar['sundays']])
