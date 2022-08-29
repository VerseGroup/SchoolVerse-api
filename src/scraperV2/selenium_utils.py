# generates a new selenium instance (various setup options)

# python imports
import os

# selenium imports for driver work
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

# selenium imports for get function
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# returns the abs path of the selenium drivers
def get_driver_path() -> dict:
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

def generate_driver(type, download=True) -> webdriver:
    
    # option to use existing driver or download a new one (local run - > use existing, external run -> download)
    if not download:
        driverpath = get_driver_path()[type]
        print("DRIVER PATH: " + driverpath + "\n")
    else:
        if type == "chrome":
            from selenium.webdriver.chrome.service import Service
            s=Service(ChromeDriverManager().install())
        elif type == "firefox":
            from selenium.webdriver.firefox.service import Service
            s=Service(GeckoDriverManager().install())

    # configuring which driver to use
    if type == "chrome":
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(service=s, options=options)
    if type == "firefox":
        driver = webdriver.Firefox(service=s)
    
    return driver

# a custom function to simplify syntax for getting with explicit waits
def get(driver, by, string):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((by, string))
        )
    except:
        driver.quit()
        raise ValueError('element could not be found')

    return element
