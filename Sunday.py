from Day import Day
from calendar import Calendar
from Presence import Presence


class Sunday(Day):

    def __init__(self, year, month, day, presence=Presence.ABSENT):
        super(Sunday, self).__init__(year, month, day)
        self.presence = presence

    def __str__(self):
        return 'Sunday(year=%s, month=%s, day=%s, presence=%s)' % (self.year, self.month, self.day, self.presence)

    def to_dict(self):
        return {
            'year': self.year,
            'month': self.month,
            'day': self.day,
            'presence': self.presence.name
        }

    @staticmethod
    def is_sunday(dt):
        return dt.weekday() == 6

    @staticmethod
    def get_sundays_from_year(year):
        days = []
        c = Calendar().yeardayscalendar(year)
        month_index = 1

        for x in c:
            for month in x:
                for week in month:
                    day = week[6]
                    if day is not 0:
                        days.append(Sunday(year, month_index, day))
                month_index += 1

        return days
