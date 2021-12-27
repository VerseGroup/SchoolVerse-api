# internal packages
import os
import sys
import json

# external packages
import requests
from bs4 import BeautifulSoup

# adding directories for local imports
parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentdir)
currentdir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(currentdir)

# local imports
from ...models import Task, Course

# load urls
from urls import SCHOOLOGY_URL, SCHOOLOGY_LOGIN_URL, SCHOOLOGY_IAPI2_URL

# schoology web scraper function that takes username and password parameters 
# and outputs the JSON formatted courses/tasks associated with that username
def scrape_schoology(username, password):
    
    # the URL session
    s = requests.Session()