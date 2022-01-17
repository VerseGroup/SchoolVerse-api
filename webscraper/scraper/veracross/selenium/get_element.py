# a custom function to simplify syntax
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get(driver, by, string):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((by, string))
        )
    except:
        #driver.close()
        pass

    return element