# python imports
import time, json, uuid
from bs4 import BeautifulSoup
from datetime import date, datetime

# internal imports
from src.config import SELENIUM_TYPE
from src.scraperV2.selenium_utils import generate_driver, get

# models
from models import Event

# URLS
VERACROSS_URL = "https://accounts.veracross.com/hackley/portals/login"

# selenium imports
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def auth_veracross(driver, username, password): 
    driver.get(VERACROSS_URL)

    username_field = get(driver, By.NAME, 'username')
    username_field.send_keys(username)

    next = get(driver, By.NAME, 'commit')
    next.click()

    password_field = get(driver, By.NAME, 'password')
    password_field.send_keys(password)

    password_field.submit()

    time.sleep(1) # seems to fix recaptcha

    # sometimes recaptcha occurs sometimes it doesn't
    try: 
        is_login_form = driver.find_element(By.ID, 'username')
        failed = True
    except:
        failed = False

    if failed:

        print("Failed, trying to reauthenticate veracross...")

        username_field = get(driver, By.NAME, 'username')
        username_field.send_keys(username)

        password_field = get(driver, By.NAME, 'password')
        password_field.send_keys(password)

        recpatcha_submit = get(driver, By.ID, 'recaptcha')
        driver.execute_script("arguments[0].removeAttribute('disabled')", recpatcha_submit)
        recpatcha_submit.click()

    return driver

# python imports

# local imports


# selenium imports


def ensure_veracross(username, password):

    TYPE = SELENIUM_TYPE
    driver = generate_driver(TYPE)
    print(f"Running {TYPE} browser\n")

    try:
        print("Authenticating veracross...\n")
        driver = auth_veracross(driver, username, password)
    except:
        raise ValueError("Probably didn't enter username or password correctly")

    try:
        driver.get("https://portals.veracross.com/hackley/student")
        driver.find_element(By.ID, "username")
        return False
    except:
        return True

def scrape_events(start_year, start_month, start_day, end_year, end_month, end_day, driver):
    url = f"https://portals.veracross.com/hackley/student/calendar/school/events?begin_date={start_month}%2F{start_day}%2F{start_year}&end_date={end_month}%2F{end_day}%2F{end_year}"
    
    print()
    print(url)
    print()

    driver.get(url)
    html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html, 'html.parser')
    data = soup.find_all('pre')[0].text
    
    return data

def parse_events(events):
    events = json.loads(events)

    parsed_events = []

    for event in events:
        start_date = event['start_date']
        end_date = event['end_date']
        start_time = event['start_time']
        end_time = event['end_time']
        description = event['description']
        location = event['location']
        name = event['tooltip']

        vc_id = event['record_identifier']
        
        link_style = event['link_style']

        try:
            link_style = link_style.split("#")[1]
        except:
            link_style = event['link_style']

        if "color:" in link_style:
            link_style = link_style.split("color: ")[1]
            if link_style == "black":
                link_style = "000000"

        link_style = "#" + str(link_style)

        
        platform_information = {
            'platform_code': 'vc',
            'event_id': vc_id,
            'link_style': link_style
        }

        id = str(uuid.uuid4())

        parsed_event = Event(id, name, location, description, start_date, start_time, end_date, end_time, platform_information=platform_information)
        parsed_events.append(parsed_event.serialize())


    #file = open('logs/events.json', 'w')
    #file.write(json.dumps(events))
    #file.close()

    return parsed_events

def get_events(username, password):

    TYPE = SELENIUM_TYPE
    driver = generate_driver(TYPE)
    print(f"Running {TYPE} browser\n")

    try:
        print("Authenticating veracross...\n")
        driver = auth_veracross(driver, username, password)
    except:
        raise ValueError("Probably didn't enter username or password correctly")

    today = date.today()
    today = today.strftime("%d/%m/%Y")
    today = today.split('/')

    day = int(today[0])
    month = int(today[1])
    year = int(today[2])\

    try:
        json_events = scrape_events(year, month, day, year, month+1, day, driver)
    except Exception as e:
        return {'message': 'failed to pull events', 'error': str(e)}

    file = open('logs/raw_events.json', 'w')
    file.write(json.dumps(json_events))
    file.close()

    events = parse_events(json_events)

    return events

# function to scrape veracross using selenium
def get_schedule(driver, day, month, year) -> str:

    SCHEDULE_URL = f"https://portals.veracross.com/hackley/student/student/daily-schedule?date={year}-{month}-{day}"
    driver.get(SCHEDULE_URL)

    schedule_page = driver.page_source

    return schedule_page

def scrape_veracross(username, password, today=True) -> tuple:

    TYPE = SELENIUM_TYPE

    print("Executing...\n")
    driver = generate_driver(TYPE)
    print(f"Running {TYPE} browser\n")

    try:
        print("Authenticating veracross...\n")
        driver = auth_veracross(driver, username, password)
    except:
        raise ValueError("Probably didn't enter username or password correctly")

    if today==True:
        today = date.today()
        today = today.strftime("%d/%m/%Y")
        today = today.split('/')

    required_days = [1, 2, 3, 4, 5, 6, 7]
    required_days_count = len(required_days)
    count = 0
    days = []

    scraping_day = int(today[0])
    scraping_month = int(today[1]) - 2 # remove -=2

    while count < 30:

        scraping_day += 1

        if scraping_day > 28:
            scraping_day = 1
            scraping_month = scraping_month + 1

        print("Getting schedule...\n")
        html = get_schedule(driver, str(scraping_day), str(scraping_month), today[2])

        print("Parsing schedule...\n")
        schedule = parse_html(html)

        print("Getting day...\n")
        try:
            day = int(get_day(html))
            schedule['day'] =  f"Day {day}"
        except:
            count += 1
            continue

        print("Found new day...\n")
        if day in required_days:
            days.append(schedule)
            required_days.remove(int(day))
            required_days_count -= 1
            print(f"FOUND day {day}...\n")

        count += 1
        print(f"Loop Iterations: {count}")
        print(f"Required Days Remaining: {required_days}" + "\n")
        print(f"Number of Required Days Remaining: {required_days_count}" + "\n")

        if required_days_count == 0:
            break

    driver.close()
    driver.quit()

    if count == 30:
        print("Couldn't find all required days...\n")

    return days

# parses pulled veracross schedule html into a specialized dict/array

# external imports


# strips a string of white space
def strip_string(string) -> str:
    stripped_string = string.replace(" ", "")
    stripped_string = stripped_string.replace("\n", "")
    return stripped_string

def add_free(period, time):
    free_template = {
        "class_name" : "Free",
        "information" : "",
    }
    free_template["start_time"] = time
    free_template["period"] = period
    if time == "12:15pm" or time == "12:45pm":
        free_template["class_name"] = "Lunch"
    return free_template

# parses veracross schedule into period objects
def parse_html(html) -> list:
    soup = BeautifulSoup(html, 'html.parser')
    schedule = soup.find("div", class_="schedule")

    log = open(f"logs/schedule.html", "w+") 
    log.write(schedule.prettify())
    log.close()

    schedule_list = []

    try:
        columns = schedule.contents
    except:
        return None

    for column in columns:

        if column.name != 'div':
            continue

        rows = column.contents

        time = rows[1].contents[0].string
        class_ = rows[3].contents[1].string
        teacher = rows[3].contents[5].string

        time = strip_string(time)
        teacher = strip_string(teacher).replace("•", "-")

        if time == '':
            continue

        if time == "8:05am":
            period_number = "Homeroom"
        elif time == "8:15am":
            period_number = "Period 1"
        elif time == "9:05am":
            period_number = "Period 2"
        elif time == "9:55am":
            period_number = "Period 3"
        elif time == "11:00am":
            period_number =  "Period 4"
        elif time == "12:15pm":
            period_number = "Period 5a"
        elif time == "12:45pm":
            period_number = "Period 5b"
        elif time == "1:30pm":
            period_number = "Period 6"
        elif time == "2:20pm":
            period_number = "Period 7"
        else:
            period_number = None

        if period_number is None:
            continue

        period = {
            "class_name" : class_,
            "information" : teacher,
            "start_time" : time,
            "period" : period_number,
        }

        schedule_list.append(period)

    full_schedule = ["Period 1", "Period 2", "Period 3", "Period 4", "Period 5a", "Period 5b", "Period 6", "Period 7"]

    for period in schedule_list:
        if period['period'] in full_schedule:
            full_schedule.remove(period['period'])

    for period in full_schedule:

        if period == "Period 1":
            time = "8:15am"
        elif period == "Period 2":
            time = "9:05am"
        elif period == "Period 3":
            time = "9:55am"
        elif period == "Period 4":
            time = "11:00am"
        elif period == "Period 5a":
            time = "12:15pm"
        elif period == "Period 5b":
            time = "12:45pm"
        elif period == "Period 6":
            time = "1:30pm"
        elif period == "Period 7":
            time = "2:20pm"
        elif period == "Homeroom":
            time = "8:05am"

        schedule_list.append(add_free(period, time))  

    sorted_schedule_list = []

    for period in schedule_list:
        period_num = period['period']
        if period_num == "Homeroom":
            period_num = 0
        else:
            period_num = period_num.replace("Period ", "")
            if period_num == "5a":
                period_num = 5
            elif period_num == "5b":
                period_num = 5.5
        period_num = float(period_num)
        period['period_num'] = period_num

    print(schedule_list)

    # sort the schedule_list array into the sorted_schedule_list array by period number
    for period in sorted(schedule_list, key=lambda k: k['period_num']):
        sorted_schedule_list.append(period)

    for period in sorted_schedule_list:
        del period['period_num']
        
    new_schedule_list = {
        "periods" : sorted_schedule_list,
    } 
        
    return new_schedule_list

# returns the day being scraped
def get_day(html) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    day_container = soup.find("h2", class_="rotation-day-header")
    day = day_container.contents[0]
    day = day.replace(" ", "")
    day = day.replace("\n", "")
    day = day.replace("Day", "")

    print(f"\n \n \n DAY: {day} \n \n \n")

    return day

# day, month two digits (ex. 01) year four digits (ex. 2020)
class SportModel:
    def __init__(self, id, start_date, start_time, end_date, end_time, description, location, link_style):
        self.id = uuid.uuid4()

        self.platform_information = {
            'platform_code': 'vc',
            'id': id,
            'link_style': link_style
        }

        self.location = location
        self.description = description
        
        self.start_date = convert_date(start_date, start_time)
        self.end_date = convert_date(end_date, end_time)

    def serialize(self):
        return {
            'id': str(self.id),
            'platform_information': self.platform_information,
            'location': self.location,
            'description': self.description,
            'start_date': self.start_date,
            'end_date': self.end_date
        }

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

def get_url(start_day, start_month, start_year, end_day, end_month, end_year):
    start_date = f"{start_month}/{start_day}/{start_year}"
    end_date = f"{end_month}/{end_day}/{end_year}"
    return f"https://portals.veracross.com/hackley/student/calendar/athletic/events?begin_date={start_date}&end_date={end_date}"

def parse_sports(html):

    soup = BeautifulSoup(html, 'html.parser')
    html = soup.find_all('pre')[0].text

    sports = json.loads(html)
    parsed_sports = []
    
    for sport in sports:
        id = sport['id']
        start_date = sport['start_date']
        start_time = sport['start_time']
        end_date = sport['end_date']
        end_time = sport['end_time']
        description = sport['description']
        location = sport['location']
        link_style = sport['link_style']

        record_type = sport['record_type']
        if record_type == 0:
            continue

        parsed_sports.append(SportModel(id, start_date, start_time, end_date, end_time, description, location, link_style).serialize())

    return parsed_sports

def get_sport_data(start_day, start_month, start_year, end_day, end_month, end_year, driver):
   
   url = get_url(start_day, start_month, start_year, end_day, end_month, end_year)
   driver.get(url)
   html = driver.page_source
   driver.quit()

   return html

def run_sports_scraper(username, password):
    TYPE = SELENIUM_TYPE
    driver = generate_driver(TYPE)
    print(f"Running {TYPE} browser\n")

    try:
        print("Authenticating veracross...\n")
        driver = auth_veracross(driver, username, password)
    except:
        raise ValueError("Probably didn't enter username or password correctly")

    today = date.today()
    today = today.strftime("%d/%m/%Y")
    today = today.split('/')

    day = int(today[0])
    month = int(today[1])
    year = int(today[2])\

    try:
        sports = get_sport_data(year, month, day, year, month+1, day, driver)
    except Exception as e:
        return {'message': 'failed to pull events', 'error': str(e)}

    file = open('logs/raw_events.json', 'w')
    file.write(json.dumps(sports))
    file.close()

    sports = parse_sports(sports)

    print(sports)

    return sports