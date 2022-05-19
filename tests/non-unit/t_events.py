# python imports
import os
import sys
from datetime import date, datetime
import json

# adding directories for local imports
parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentdir)
currentdir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(currentdir)
tripleparentdir = os.path.abspath(os.path.join(parentdir, os.path.pardir))
sys.path.append(tripleparentdir)

# imports
from src.webscraper.scraper.veracross.events import get_events
from getpass import getpass

def convert_date(date, time):

    if date is None:
        return None
    
    date = date.split("/")
    
    month = date[0]
    day = str(int(date[1]) + 1) # bug where dates are off by one
    year = date[2]

    if time is None:
        return str(datetime(int(year), int(month), int(day)))

    times = time.split(" ")
    
    time = times[0].split(":")
    hour = time[0]
    minute = time[1]

    am_pm = times[1]
    if am_pm == "PM" and hour != "12":
        hour = int(hour) + 12

    date_object = datetime(int(year), int(month), int(day), int(hour), int(minute))
    
    return str(date_object)


def test_events():
    username = input('Username: ')
    password = getpass()

    return get_events(username, password)
    
if __name__ == '__main__':
    events = test_events()

    formated_events = []

    for event in events:

        doc_name = f"{event['id']}"
        
        try:
            start = convert_date(event['start_date'], event['start_time'])
            end = convert_date(event['end_date'], event['end_time'])
        except Exception as e:
            start = f"something broke with error {str(e)}"
            end = f"something broke with error {str(e)}"

        event.pop('start_date')
        event.pop('start_time')
        event.pop('end_date')
        event.pop('end_time')
        
        event['start'] = start
        event['end'] = end

        if "Day" in event['description'] and len(event['description']) == 5:
            event.pop('location')
            event.pop('end')
            event.pop('description')
            event['day'] = event['name']
            event.pop('name')
            event['date'] = event['start']
            event.pop('start')

        formated_events.append(event)


    print(json.dumps(formated_events))
