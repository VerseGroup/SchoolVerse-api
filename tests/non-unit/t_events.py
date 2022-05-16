# python imports
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
from src.webscraper.scraper.veracross.events import get_events
from getpass import getpass


def test_events():
    username = input('Username: ')
    password = getpass()

    return get_events(username, password)
    
if __name__ == '__main__':
    events = test_events()
    print(events)
