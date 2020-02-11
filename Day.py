class Day:

    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def __str__(self):
        return 'Day(year=%s, month=%s, day=%s)' % (self.year, self.month, self.day)

    def __eq__(self, day):
        return self.year == day.year and self.month == day.month and self.day == day.day

    def to_dict(self):
        return {
            'year': self.year,
            'month': self.month,
            'day': self.day
        }
