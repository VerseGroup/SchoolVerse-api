# python imports
import time, json, uuid
from bs4 import BeautifulSoup
from datetime import date, datetime

# internal imports
from src.config import SELENIUM_TYPE
from src.scraperV2.selenium_utils import generate_driver, get

# models
from src.models import Event

# URLS
VERACROSS_URL = "https://accounts.veracross.com/hackley/portals/login"

# selenium imports
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

### Start Selenium ###

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

        # get past recaptcha
        recpatcha_submit = get(driver, By.ID, 'recaptcha')
        driver.execute_script("arguments[0].removeAttribute('disabled')", recpatcha_submit)
        recpatcha_submit.click()

    return driver

### Ensure Veracross ###

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


        