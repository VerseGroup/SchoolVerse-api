# python/external imports
import requests

# internal imports
from src.webscraper.scraper.schoology.urls import SCHOOLOGY_LOGIN_URL

def auth_schoology(username, password) -> requests.Session:
    
    # the URL session to scrape from
    s = requests.Session()

    # login fields
    login_params = f"mail={username}&pass={password}&school_nid=1938279719&form_id=s_user_login_form"
    login_headers =  {"Content-Type" : "application/x-www-form-urlencoded"}

    # login post request
    response = s.post(url=SCHOOLOGY_LOGIN_URL, data=login_params, headers=login_headers)
    print(f"Login Status: {response.status_code}") 

    return s