# This file contains the function that scrapes schoology assignments/courses using a username/passeord

# Todo #
# - Add checks in case login failed 
# - Add a lot more try/excepts for other errors
# - Finish copying over parsers, scrapers, etc from SchoolVerse testing
# - Intead of returning a dictionary of tasks, return serialized course objects instead

# internal packages
import os
import sys
import json

# external packages
import requests

# adding directories for local imports
parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentdir)
currentdir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(currentdir)

# local imports
from ...models import Task, Course
from parse_courses import parseCourses
from parse_html import parseHTML

# load urls
from urls import SCHOOLOGY_URL, SCHOOLOGY_LOGIN_URL, SCHOOLOGY_IAPI2_URL

# schoology web scraper function that takes username and password parameters 
# and outputs the JSON formatted courses/tasks associated with that username
def scrape_schoology(username, password):
    
    # the URL session to scrape from
    s = requests.Session()

    # login fields
    login_params = f"mail={username}&pass={password}&school_nid=1938279719&form_id=s_user_login_form"
    login_headers =  {"Content-Type" : "application/x-www-form-urlencoded"}

    # login post request
    response = s.post(url=SCHOOLOGY_LOGIN_URL, data=login_params, headers=login_headers)
    print(f"Login Status: {response.status_code}")  

    # getting user associated coure codes with IAPI2
    response = s.get(url=SCHOOLOGY_IAPI2_URL)
    courses = parseCourses(json.loads(response.text))

    tasks = {}

    # get materials for each course
    for course_object in courses:

        # getting the material page for the course
        course_id = course_object.schoology_id
        url = f"{SCHOOLOGY_URL}/course/{course_id}/calendar_ajax?original_q=course/{course_id}/materials" 

        # decoding unicode into something beautiful soup can understand
        response = s.get(url)
        content = response.content
        decoded_content = content.decode('unicode-escape').replace("\/", "/")
        html = str(decoded_content)[1: -1]

        # parsing file into serialized task objects
        parsed_tasks = parseHTML(html)
        
        # adding to dict 
        tasks[course_object.name] = parsed_tasks

    return tasks