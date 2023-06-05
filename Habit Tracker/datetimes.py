import datetime as dt
import calendar
from constants import months, day_names_list, get_days_in_month


def month_days(month=dt.datetime.now().month, year=dt.datetime.now().year):
    day = dt.datetime.isoweekday(dt.date(year, month, 1))
    days_in_month = {m1 + 1: (months[m1], calendar.monthrange(year, m1 + 1)[1]) for m1 in
                     range(len(months))}
    return days_in_month[month][0], days_in_month[month][1], month, year, day + 1


def date_passed(date, month, year):
    now_x = dt.datetime.now().date()
    print(now_x)
    target_x = dt.datetime(year, month, date).date()
    return now_x >= target_x