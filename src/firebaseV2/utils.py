from datetime import datetime

def convert_date(date, time):

    if date is None:
        return None
    
    date = date.split("/")
    
    month = date[0]
    day = str(int(date[1]) + 1) # bug where dates are off by one
    year = date[2]

    if time is None:
        return datetime(int(year), int(month), int(day))

    times = time.split(" ")
    
    time = times[0].split(":")
    hour = time[0]
    minute = time[1]

    am_pm = times[1]
    if am_pm == "PM" and hour != "12":
        hour = int(hour) + 12

    date_object = datetime(int(year), int(month), int(day), int(hour), int(minute))
    
    return date_object

def convert_flik_date(date):
    date = date.split('-')
    year = date[0]
    month = date[1]
    day = int(date[2]) 

    return datetime(int(year), int(month), int(day), 12, 0, 0)
