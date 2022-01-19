# python imports
import os

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
    driver_dir = driver_dir[1:]
    return {
        "firefox" : f'{driver_dir}/driver/geckodriver',
        "chrome" : f'{driver_dir}/driver/chromedriver',
    }

def generate_driver(type):
    
    driverpath = get_driver_path()[type]
    print("DRIVER PATH: " + driverpath + "\n")

    if type == "chrome":
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(driverpath, options=options)
    if type == "firefox":
        s=Service(driverpath)
        driver = webdriver.Firefox(service=s)
    
    return driver