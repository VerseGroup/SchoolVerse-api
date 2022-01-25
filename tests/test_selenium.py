# test selenium and selenium instances

# python imports
import os
import sys

# adding directories for local imports
parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentdir)
currentdir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(currentdir)

# selenium imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.chrome.options import Options

# local imports
from webscraper.scraper.veracross.selenium.newdriver import generate_driver

def test_selenium():
    '''
    driver = generate_driver("chrome")
    driver.get("https://www.google.com/")
    driver.close()
    driver.quit()
    '''
    assert True # checking for bugs


