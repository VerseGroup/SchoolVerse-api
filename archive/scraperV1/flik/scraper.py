""" # external imports
import requests

# local imporst
from src.webscraper.scraper.flik.urls import get_flik_url
from src.webscraper.scraper.flik.parse import parse_menu

def get_flik_data(type, day, month, year):

    # request for data
    url = get_flik_url(type, year, month, day)
    response = requests.get(url)
    if response.status_code != 200:
        return None
    response_text = response.text

    # log data
    #file = open("logs/menu.json", "a")
    #file.write(response_text)
    #file.close()

    return response_text

def scrape_flik(day, month, year):

    breakfast = get_flik_data("breakfast", day, month, year)
    lunch = get_flik_data("lunch", day, month, year)
    dinner = get_flik_data("dinner", day, month, year)

    menu = parse_menu(breakfast, lunch, dinner)

    return menu



    

 """