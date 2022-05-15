# external imports
from platform import platform
from bs4 import BeautifulSoup
import json
import uuid

# python imports
from datetime import date

# local imports
from src.webscraper.scraper.veracross.auth import auth_veracross
from src.webscraper.scraper.veracross.driver import generate_driver
from src.webscraper.models import Event
from src.config import SELENIUM_TYPE

# selenium imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

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
