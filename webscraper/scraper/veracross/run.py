# function to scrape veracross using selenium

# python imports
import os
import sys
import time
from datetime import date

# adding parent directory to potential package locations 
currentdir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(currentdir)

# internal imports
from get_element import get
from schedule import parse_html, get_day
from driver import generate_driver
from veracross.auth import auth_veracross

# selenium imports
from selenium.webdriver.common.by import By

def scrape_schedule(driver, day, month, year):

    SCHEDULE_URL = f"https://portals.veracross.com/hackley/student/student/daily-schedule?date={year}-{month}-{day}"
    driver.get(SCHEDULE_URL)

    schedule_page = driver.page_source
    driver.close()
    driver.quit()

    return schedule_page

def scrape_veracross(username, password, today=True):

    TYPE = "chrome"

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
    html = scrape_schedule(driver, today[0], today[1], today[2])

    print("Parsing schedule contents...\n")
    schedule = parse_html(html)

    print("Finding day...")
    try:
        day = get_day(html)
    except:
        day = "N/A"
    
    return (day, schedule)




