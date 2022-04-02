# function to scrape veracross using selenium

# python imports
import time
from datetime import date

# internal imports
from webscraper.scraper.veracross.get_element import get
from webscraper.scraper.veracross.schedule import parse_html, get_day
from webscraper.scraper.veracross.driver import generate_driver
from webscraper.scraper.veracross.auth import auth_veracross
from webscraper.scraper.veracross.events import scrape_events
from config import SELENIUM_TYPE


# selenium imports
from selenium.webdriver.common.by import By

def get_schedule(driver, day, month, year) -> str:

    SCHEDULE_URL = f"https://portals.veracross.com/hackley/student/student/daily-schedule?date={year}-{month}-{day}"
    driver.get(SCHEDULE_URL)

    schedule_page = driver.page_source
    driver.close()
    driver.quit()

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

    print("Gathering schedule contents...\n")
    html = get_schedule(driver, str(int(today[0])+3), today[1], today[2])

    print("Parsing schedule contents...\n")
    schedule = parse_html(html)

    print("Finding day...")
    try:
        day = get_day(html)
    except:
        day = "N/A"

    return (day, schedule)



