# external imports
import requests

# local imporst
from webscraper.scraper.flik.urls import get_flik_url
from webscraper.scraper.flik.parse import parse_menu

def scrape_flik(type, day, month, year):

    # request for data
    url = get_flik_url(type, year, month, day)
    response = requests.get(url)
    if response.status_code != 200:
        return None
    response_text = response.text

    # log data
    file = open("logs/menu.json", "a")
    file.write(response_text)
    file.close()

    # parse data
    menu = parse_menu(response.json())

    return menu
    

