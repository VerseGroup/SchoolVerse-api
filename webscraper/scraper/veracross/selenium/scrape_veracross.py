# python imports
import os
import sys
import time
from datetime import date

# adding parent directory to potential package locations 
parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentdir)
currentdir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(currentdir)

# internal imports
from get_element import get

# external imports
from getpass import getpass

# selenium imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.service import Service

GECKO_DRIVER_PATH = '/Users/pevans/Documents/SchoolVerse-webscraper/driver/geckodriver'
VERACROSS_URL = "https://accounts.veracross.com/hackley/portals/login"

def auth_veracross(username, password):
    s=Service(GECKO_DRIVER_PATH)
    driver = webdriver.Firefox(service=s)
    driver.maximize_window() # remove
    driver.get(VERACROSS_URL)

    username_field = get(driver, By.NAME, 'username')
    username_field.send_keys(username)

    password_field = get(driver, By.NAME, 'password')
    password_field.send_keys(password)

    password_field.submit()

    time.sleep(1) # seems to fix recaptcha

    # sometimes recaptcha occurs sometimes it doesn't
    try: 
        is_login_form = driver.find_element(By.ID, 'username')

        username_field = get(driver, By.NAME, 'username')
        username_field.send_keys(username)

        password_field = get(driver, By.NAME, 'password')
        password_field.send_keys(password)

        recpatcha_submit = get(driver, By.ID, 'recaptcha')
        driver.execute_script("arguments[0].removeAttribute('disabled')", recpatcha_submit)
        recpatcha_submit.click()
    except:
        pass

    return driver

def scrape_schedule(driver, day, month, year):

    SCHEDULE_URL = f"https://portals.veracross.com/hackley/student/student/daily-schedule?date={year}-{month}-{day}"
    driver.get(SCHEDULE_URL)
    

if __name__ == '__main__':
    USERNAME = input('USERNAME: ')
    PASSWORD = getpass()
    try:
        driver = auth_veracross(USERNAME, PASSWORD)
    except:
        raise ValueError("Probably didn't enter username or password correctly")

    today = date.today()
    today = today.strftime("%d/%m/%Y")
    today = today.split('/')

    scrape_schedule(driver, today[0], today[1], today[2])




