from datetime import datetime

class Day:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def __str__(self, separator='/'):
        return '%s%s%s%s%s' % (self.year, separator, str(self.month).rjust(2,'0'), separator, str(self.day).rjust(2,'0'))

    def __repr__(self):
        return 'Day(year=%s, month=%s, day=%s)' % (self.year, self.month, self.day)

    def __lt__(self, day):
        return self.year <= day.year and self.month <= day.month and self.day < day.day

    def __le__(self, day):
        return self.year <= day.year and self.month <= day.month and self.day <= day.day

    def __gt__(self, day):
        return self.year >= day.year and self.month >= day.month and self.day > day.day

    def __ge__(self, day):
        return self.year >= day.year and self.month >= day.month and self.day >= day.day

    def __eq__(self, day):
        return self.year == day.year and self.month == day.month and self.day == day.day

    def __ne__(self, day):
        return self.year != day.year or self.month != day.month or self.day != day.day

    def to_dict(self):
        return {
            'year': self.year,
            'month': self.month,
            'day': self.day
        }

    @staticmethod
    def today():
        today = datetime.today()
        return Day(today.year, today.month, today.day)

    @staticmethod
    def from_dict(day):
        return Day(day['year'], day['month'], day['day'])

    @staticmethod
    def from_str(day):
        if '-' in day:
            day = day.split('-')
        elif '/' in day:
            day = day.split('/')
        return Day(int(day[0]), int(day[1]), int(day[2]))
