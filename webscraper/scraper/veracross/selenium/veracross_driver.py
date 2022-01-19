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
from parse_vc_html import parse_html

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
from selenium.webdriver.chrome.options import Options

def get_driver_path():
    this_file = os.path.dirname(os.path.abspath(__file__))
    this_file = this_file.split('/')
    driver_dir = ""
    for i in range(5):
        driver_dir += f"/{this_file[i]}"
    return {
        "firefox" : f'{driver_dir}/driver/geckodriver',
        "chrome" : f'{driver_dir}/driver/chromedriver',
    }

def generate_driver(type):
    
    driverpath = get_driver_path()[type]
    print(driverpath)

    if type == "chrome":
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(driverpath, options=options)
    if type == "firefox":
        s=Service(driverpath)
        driver = webdriver.Firefox(service=s)
    
    return driver

VERACROSS_URL = "https://accounts.veracross.com/hackley/portals/login"

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

        username_field = get(driver, By.NAME, 'username')
        username_field.send_keys(username)

        password_field = get(driver, By.NAME, 'password')
        password_field.send_keys(password)

        recpatcha_submit = get(driver, By.ID, 'recaptcha')
        driver.execute_script("arguments[0].removeAttribute('disabled')", recpatcha_submit)
        recpatcha_submit.click()

    return driver

def scrape_schedule(driver, day, month, year):

    SCHEDULE_URL = f"https://portals.veracross.com/hackley/student/student/daily-schedule?date={year}-{month}-{day}"
    driver.get(SCHEDULE_URL)

    schedule_page = driver.page_source
    driver.close()
    driver.quit()

    return schedule_page

def scrape_veracross(username, password, today=True):
    driver = generate_driver("chrome")

    try:
        driver = auth_veracross(driver, USERNAME, PASSWORD)
    except:
        raise ValueError("Probably didn't enter username or password correctly")

    if today==True:
        today = date.today()
        today = today.strftime("%d/%m/%Y")
        today = today.split('/')

    html = scrape_schedule(driver, today[0], today[1], today[2])

    schedule = parse_html(html)
    
    return schedule

if __name__ == '__main__':
    USERNAME = input('USERNAME: ')
    PASSWORD = getpass()

    start_time = time.time()
    
    schedule = scrape_veracross(USERNAME, PASSWORD)
    
    print()
    print(schedule)

    print()
    print(f"Executed in {time.time() - start_time} seconds")




