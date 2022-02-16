# external imports
from bs4 import BeautifulSoup
import json

# python imports
from datetime import date

# local imports
from webscraper.scraper.veracross.auth import auth_veracross
from webscraper.scraper.veracross.driver import generate_driver
from config import SELENIUM_TYPE

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
    
    json_data = data.json()
    return json_data

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
    except:
        return {'message': 'failed to pull events'}

    file = open('logs/events.json', 'w')
    file.write(json.dumps(json_events))
    file.close()

    return json_events
