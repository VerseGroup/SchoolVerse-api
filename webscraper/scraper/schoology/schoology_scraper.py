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
from parse_courses import parseCourses
from parse_html import parse_html
from descriptions import parse_descriptions
from schoology.auth import auth_schoology

# load urls
from urls import SCHOOLOGY_URL, SCHOOLOGY_LOGIN_URL, SCHOOLOGY_IAPI2_URL


# schoology web scraper function that takes username and password parameters 
# and outputs the JSON formatted courses/tasks associated with that username
def scrape_schoology(username, password):
    
    s = auth_schoology(username, password)

    # getting user associated coure codes with IAPI2
    response = s.get(url=SCHOOLOGY_IAPI2_URL)
    courses = parseCourses(json.loads(response.text))

    tasks = []

    # get materials for each course
    for course_object in courses:

        # getting the material page for the course
        course_id = course_object.platform_information['course_code']
        url = f"{SCHOOLOGY_URL}/course/{course_id}/calendar_ajax?original_q=course/{course_id}/materials" 

        # decoding unicode into something beautiful soup can understand
        response = s.get(url)
        content = response.content

        # logging raw received content
        '''
        test_log = open(f"scraper_logs/RAW: {course_object.serialize()['name']}.html", "w+") 
        test_log.write(content.decode('utf-8'))
        test_log.close()
        '''

        decoded_content = content.decode('unicode-escape').replace("\/", "/")
        html = str(decoded_content)[1: -1]

        # logging content exactly as to be scraped for unit testing
        test_log = open(f"logs/scraping/SCRAPING_FORMATTED: {course_object.serialize()['name']}.html", "w+") 
        test_log.write(html)
        test_log.close()
        

        # logging pretty content to be used for debugging
        logging_soup = BeautifulSoup(html, 'html.parser')
        test_log = open(f"logs/scraping/pretty/PRETTY: {course_object.serialize()['name']}.html", "w+") 
        test_log.write(logging_soup.prettify())
        test_log.close()

        # parsing file into serialized task objects
        print(f"{course_object.serialize()['name']}: ")
        parsed_tasks = parse_html(html, course_object)
        print()
        
        # adding to dict 
        tasks = tasks + parsed_tasks

    #tasks = parse_descriptions(tasks, s)

    return tasks

