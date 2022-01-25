# This file contains the function that scrapes schoology assignments/courses using a username/passeord

# Todo #
# - Add checks in case login failed 
# - Add a lot more try/excepts for other errors
# - Finish copying over parsers, scrapers, etc from SchoolVerse testing
# - Intead of returning a dictionary of tasks, return serialized course objects instead

# internal imports
import os
import sys
import json

# external imports
import requests
from bs4 import BeautifulSoup

# adding directories for local imports
parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentdir)
doubleparentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir))
sys.path.append(doubleparentdir)
tripleparentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir, os.path.pardir))
sys.path.append(tripleparentdir)
currentdir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(currentdir)

# local imports
from models import Task, Course
from courses import parse_courses
from schoology.auth import auth_schoology

# load urls
from urls import SCHOOLOGY_URL, SCHOOLOGY_IAPI2_URL

# schoology webscraper
def scrape_schoology(username, password):
    
    s = auth_schoology(username, password)

    # getting user associated coure codes with IAPI2
    response = s.get(url=SCHOOLOGY_IAPI2_URL)
    try:
        courses = parse_courses(json.loads(response.text))
    except:
        return None
