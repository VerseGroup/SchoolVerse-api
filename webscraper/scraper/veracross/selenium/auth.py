# python imports
import os
import sys
import time

# adding parent directory to potential package locations 
parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentdir)
currentdir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(currentdir)

# internal imports
'''
from keys import GECKO_DRIVER_PATH
from urls import 
from get_element import get
'''

# selenium imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

def auth_veracross():
    #driver = webdriver.Firefox(executable_path=GECKO_DRIVER_PATH)
    #driver.maximize_window()
    pass