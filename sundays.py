import calendar
import datetime

def is_sunday(dt):
    return dt.weekday() == 6

def get_sundays_from_month(month, month_index):
    days = []

    for week in month:
        day = week[6]
        if day is not 0:
            s = '%s-%s' % (month_index, day)
            days.append(s)

    return days

def get_sundays_from_year(year=datetime.datetime.now().year):
    days = []
    c = calendar.Calendar().yeardayscalendar(year)
    month_index = 1

    for something in c:
        for month in something:
            days += get_sundays_from_month(month, month_index)
            month_index += 1

    return days

if __name__ == '__main__':
    print(get_sundays_from_year())
