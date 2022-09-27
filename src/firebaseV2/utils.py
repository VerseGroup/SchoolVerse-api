from datetime import datetime

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

    if int(hour) + 5 > 24:
        day = str(int(day) + 1)
    
    hour = str(int(hour) + 5)

    return datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))

def convert_flik_date(date):
    date = date.split('-')
    year = date[0]
    month = date[1]
    day = int(date[2]) 

    return datetime(int(year), int(month), int(day), 12, 0, 0)
