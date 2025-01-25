import datetime
from database.ConfigCollection import ConfigCollection


class Calendar:
    def __init__(self, calendar=[]):
        self.config_db = ConfigCollection()
        self.calendar = calendar

    def _find_sundays(self):
        return {
            int(timestamp)
            for entry in self.calendar
            for timestamp in entry.keys()
            if self._is_sunday(int(timestamp))
        }

    def _is_sunday(self, ts):
        return datetime.datetime.fromtimestamp(ts).weekday() == 6

    # TODO: consider justified (Presence entity)
    def is_active(self):
        today = datetime.date.today()
        first_day_of_year = datetime.date(today.year, 1, 1)
        sundays = 0

        current_day = first_day_of_year
        while current_day <= today:
            if current_day.weekday() == 6:
                sundays += 1
            current_day += datetime.timedelta(days=1)

        if sundays == 0:
            return False

        presence_rate = len(self._find_sundays()) / sundays
        return presence_rate >= self.config_db.get_active_rate()

    def to_dict(self):
        return self.calendar

    @staticmethod
    def from_dict(calendar=[]):
        return Calendar(calendar=calendar)
