# This file contains the function that scrapes schoology assignments/courses using a username/passeord

# Todo #
# - Add checks in case login failed 
# - Add a lot more try/excepts for other errors

# internal imports
import json
import time
from datetime import datetime

# local imports
from webscraper.models import Task, Course
from webscraper.scraper.schoology.courses import parse_courses
from webscraper.scraper.schoology.auth import auth_schoology
from webscraper.scraper.schoology.calender import parse_calender

# load urls
from webscraper.scraper.schoology.urls import SCHOOLOGY_IAPI2_URL

# schoology webscraper
def scrape_schoology(username, password, do_courses=True) -> dict:
    
    s = auth_schoology(username, password)

    # user courses 
    if do_courses:
        response = s.get(url=SCHOOLOGY_IAPI2_URL)
        jsonresponse = json.loads(response.text)
        try:
            courses = parse_courses(jsonresponse)
        except:
            return None
    

    # dates to scrapre
    year = str(datetime.now().year)
    month = str(datetime.now().month)
    unixstart = time.time()
    unixend = unixstart + 1209600.0

    # formatting dates
    if len(month) == 1:
        month = "0" + month

    unixstart = int(unixstart)
    unixend = int(unixend)

    # pulling calender information
    schoology_calender_url = f"https://hackley.schoology.com/calendar/{year}-{month}?ajax=1&start={unixstart}&end={unixend}"
    response = s.get(url=schoology_calender_url)
    jsonresponse = json.loads(response.text)

    parsed_content = parse_calender(jsonresponse)
    events = parsed_content['events']
    tasks = parsed_content['tasks']

    to_return = {
        "tasks" : tasks,
        "events" : events,
    }
    if courses:
        to_return["courses"] = courses

    return to_return
