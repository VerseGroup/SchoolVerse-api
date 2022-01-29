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

# URLS
VERACROSS_URL = "https://accounts.veracross.com/hackley/portals/login"

# selenium imports
from selenium.webdriver.common.by import By

def auth_veracross(driver, username, password): 
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