# python imports
import os
import sys
from datetime import date

# adding directories for local imports
parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentdir)
currentdir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(currentdir)

# imports
from webscraper.scraper.flik.scraper import scrape_flik

def test_flik(doPrint=False):

    today = date.today()
    today = today.strftime("%d/%m/%Y")
    today = today.split('/')

    day = int(today[0])
    month = int(today[1])
    year = int(today[2])
    
    menu = scrape_flik(day, month, year)
    if doPrint:
        print(menu)

    assert True # testing bugs

if __name__ == '__main__':
    test_flik(doPrint=True)