from datetime import datetime
from config import active_rate
from entities.Presence import Presence
from entities.Sunday import Sunday
from entities.Day import Day


class Calendar:

    def __init__(self, sundays=None, year=datetime.now().year):
        self.sundays = sundays if sundays is not None else Sunday.get_sundays_from_year(year)
        self.year = year

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
        size = self.sundays_length_until_today()
        if size == 0:
            return False
        return True if self.presence_count() / size >= active_rate else False

    def presence_count(self):
        count = 0
        today = Day.today()
        for sunday in self.sundays:
            if sunday > today:
                break
            if sunday.presence == Presence.PRESENT:
                count += 1
        return count

    def sundays_length_until_today(self):
        length = 0
        today = Day.today()
        for sunday in self.sundays:
            if sunday > today:
                break
            length += 1
        return length

    def to_dict(self):
        return {
            'sundays': [x.to_dict() for x in self.sundays]
        }

    @staticmethod
    def from_dict(calendar):
        return Calendar([Sunday.from_dict(x) for x in calendar['sundays']])
