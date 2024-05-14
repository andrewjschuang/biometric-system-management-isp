import datetime
import config


class Calendar:
    def __init__(self, calendar={}, year=datetime.datetime.now().year):
        self.calendar = calendar
        if len(self.calendar) == 0:
            self._init_calendar(year)

    def _init_calendar(self, year):
        start_date = datetime.date(year, 1, 1)
        end_date = datetime.date(year, 12, 31)
        delta = datetime.timedelta(days=1)
        current_date = start_date
        while current_date <= end_date:
            self.calendar[current_date.strftime("%Y-%m-%d")] = False
            current_date += delta

    def _find_sundays(self):
        return [date for date, _ in self.calendar.items() if self._is_sunday(date)]

    def _is_sunday(self, date):
        return datetime.datetime.strptime(date, "%Y-%m-%d").weekday() == 6

    def mark_presence(self, timestamp):
        if isinstance(timestamp, list):
            for t in timestamp:
                self.mark_presence(t)

        date = datetime.date.fromtimestamp(timestamp).strftime("%Y-%m-%d")
        if date in self.calendar:
            self.calendar[date] = True

    # TODO: consider justified (Presence entity)
    def is_active(self):
        sundays = self._find_sundays()
        present_sundays = [date for date in sundays if self.calendar[date]]
        presence_rate = len(present_sundays) / len(sundays)
        return presence_rate >= config.active_rate

    def to_dict(self):
        return self.calendar

    @staticmethod
    def from_dict(calendar={}):
        return Calendar(calendar=calendar)
