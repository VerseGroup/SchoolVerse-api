from datetime import datetime
import pytz

MONTHS_WITH_30 = [4, 6, 9, 11]
MONTHS_WITH_31 = [1, 3, 5, 7, 8, 10, 12]
MONTHS_WITH_29 = [2]

def convert_date(date):

    date = date.split(' ')
    time = date[1]
    date = date[0]

    date = date.split('-')
    year = date[0]
    month = date[1]
    day = date[2]

    time = time.split(':')
    hour = time[0]
    minute = time[1]
    second = time[2]

    if int(minute) == 59:
        second = 30      

    hour = str(int(hour) + 4)

    if int(hour) > 24:
        day = str(int(day) + 1)

        if int(month) in MONTHS_WITH_30:
            if int(day) > 30:
                day = '1'
                month = str(int(month) + 1)

        elif int(month) in MONTHS_WITH_31:
            if int(day) > 31:
                day = '1'
                month = str(int(month) + 1)

        elif int(month) in MONTHS_WITH_29:
            if int(day) > 29:
                day = '1'
                month = str(int(month) + 1)

        hour = str(int(hour) - 24)

        if int(hour) == 3:
            minute = 59

    return datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))

def convert_flik_date(date):
    date = date.split('-')
    year = date[0]
    month = date[1]
    day = int(date[2]) 

    return datetime(int(year), int(month), int(day), 12, 0, 0)
