# python imports
from operator import ge
import os
import sys
from datetime import date

# adding directories for local imports
parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentdir)
currentdir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(currentdir)
tripleparentdir = os.path.abspath(os.path.join(parentdir, os.path.pardir))
sys.path.append(tripleparentdir)

# imports
from webscraper.scraper.veracross.events import get_events
from getpass import getpass


def test_events():
    username = input('Username: ')
    password = getpass()

    today = date.today()
    today = today.strftime("%d/%m/%Y")
    today = today.split('/')

    day = int(today[0])
    month = int(today[1])
    year = int(today[2])

    events = get_events(username, password)
    return events

if __name__ == '__main__':
    events = test_events()
    print(events)
