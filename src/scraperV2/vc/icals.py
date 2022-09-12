# python imports
import time, json
from bs4 import BeautifulSoup
from datetime import date, datetime

# internal imports
from src.config import SELENIUM_TYPE
from src.scraperV2.selenium_utils import generate_driver, get
from src.scraperV2.vc.auth import auth_veracross

# selenium imports
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

### Scrape Veracross ###
# this function specifically gets the users daily schedule

def get_icals(username, password):

    TYPE = "firefox"

    TARGET_LINK = "https://portals.veracross.com/hackley/student/calendar/subscribe/school"

    driver = generate_driver(TYPE)
    print(f"Selenium Running {TYPE} browser\n")

    try:
        driver = auth_veracross(driver, username, password)
    except:
        raise ValueError("Probably didn't enter username or password correctly")

    driver.get(TARGET_LINK)

    html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html, 'html.parser')

    # scrape through the links in the soup and get the ical links
    ical_links = []
    for link in soup.find_all('a'):
        if link.get('href') and 'webcal' in link.get('href'):
            ical_links.append(link.get('href'))

    ical_links.pop(0)

    for link in ical_links:
        link.replace("webcal", "http")
    
    return ical_links
