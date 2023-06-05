import calendar

month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
               'November',
               'December']
year = 2023
months = [i + 1 for i in range(12)]
day_names_list = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']


def get_days_in_month(year):
    days_in_month = {m1 + 1: calendar.monthrange(year, m1 + 1)[1] for m1 in
                     range(len(months))}
    return days_in_month
