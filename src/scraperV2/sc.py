# Schoology scraping script

# URLS
SCHOOLOGY_LOGIN_URL = "https://hackley.schoology.com/login/ldap?&school=1938279719"
SCHOOLOGY_URL = "https://hackley.schoology.com"
SCHOOLOGY_IAPI2_URL = "https://hackley.schoology.com/iapi2/site-navigation/courses?includeAll=1"

# python/external imports
import requests
from datetime import datetime
import markdownify as md 
import uuid, json, time

# models
from src.models import Event, Task, Course, Temp_Event

# generate an authenticated schoology request session
def auth_schoology(username, password) -> requests.Session:
    
    # the URL session to scrape from
    s = requests.Session()

    # login fields
    login_params = f"mail={username}&pass={password}&school_nid=1938279719&form_id=s_user_login_form"
    login_headers =  {"Content-Type" : "application/x-www-form-urlencoded"}

    # login post request
    response = s.post(url=SCHOOLOGY_LOGIN_URL, data=login_params, headers=login_headers)
    print(f"Login Status: {response.status_code}") 

    return s

def parse_event(event) -> Temp_Event:
    return Temp_Event(id=event['id'], name=event['title'], date=event['start']).serialize()

def parse_task(task) -> Task:
    platform_information={
        "platform_code" : "sc",
        "assignment_code": task['content_id'],
    }
    description = task['body']
    
    # converting html description to markdown so it can be displayed in the app
    description = md.markdownify(description)

    return Task(name=task['titleText'], due_date=task['start'], course_id=task['realm_id'], course_name=task['content_title'], platform_information=platform_information, description=description).serialize()

def parse_calender(calender_json) -> dict:

    events = []
    tasks = []

    for object in calender_json:

        # check to make sure relevant date
        objectday = int(object['start'].split(" ")[0].split("-")[0])
        todaysday = datetime.now().day
        if todaysday > objectday:
            continue
        
        if object['e_type'] == "event":
            events.append(parse_event(object))
        elif object['e_type'] == "assignment":
            tasks.append(parse_task(object))

    return {
        "events" : events,
        "tasks" : tasks,
    }

# parses schoology given course information into SchoolVerse course objects
def parse_courses(courses_json) -> list:

    # isolating course from JSON
    course_array = (courses_json['data'])['courses']

    # array to hold returned objects
    course_object_array = []

    # iterating through JSON array of Schoology formatted courses
    for course in course_array:
        
        # pulling information
        name = course["courseTitle"]
        section = course["sectionTitle"]
        course_code = course["nid"]
        id = str(uuid.uuid4())

        # converting schoology_id into standerd platform information
        platform_information = {
            "code" : "sc",
            "course_code" : course_code
        }

        # writing information to a course object
        course_object = Course(id=id, name=name, section=section, platform_information=platform_information)

        # adding course object to array
        course_object_array.append(course_object)

    return course_object_array

# making sure that the schoology username and password are correct
def ensure_schoology(username, password):
    s = auth_schoology(username, password)

    response = s.get('https://hackley.schoology.com/home')
    content = response.text

    if '<span class="h3 sign-in-header">Sign in to Schoology</span>' in content:
        return False
    else:
        return True

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

    # dates to scrape
    year = str(datetime.now().year)
    month = str(datetime.now().month)
    unixstart = time.time()

    # two weeks in seconds
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

