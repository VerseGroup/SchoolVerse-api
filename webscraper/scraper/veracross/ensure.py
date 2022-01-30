# python imports
import os
import sys

# appendig dir to sys to allow local importing
currentdir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(currentdir)
parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentdir)

# local imports
from veracross.auth import auth_veracross
from veracross.driver import generate_driver

# selenium imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def ensure_veracross(username, password):

    TYPE = "chrome"
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
        return {'message': 'failed to authenticate', 'code': '1'}
    except:
        return {'message': 'success', 'code': '0'}
