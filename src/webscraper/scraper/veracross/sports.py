# external imports
from bs4 import BeautifulSoup
import json
import uuid

# python imports
from datetime import date, datetime

# local imports
from src.webscraper.scraper.veracross.auth import auth_veracross
from src.webscraper.scraper.veracross.driver import generate_driver
from src.config import SELENIUM_TYPE

# selenium imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

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

    return sports