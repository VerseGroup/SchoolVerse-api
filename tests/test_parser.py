# python imports
import os
import sys

# adding directories for local imports
parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentdir)
currentdir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(currentdir)

# local imports
from webscraper.scraper.schoology.parse_html import parse_html

TESTFILES = [
    'logs/scraping/SCRAPING_FORMATTED: POST-AP MOBILE APP DEVELOPMENT - MAJOR.html',
    'logs/scraping/SCRAPING_FORMATTED: AP CALCULUS AB & BC.html',
    'logs/scraping/SCRAPING_FORMATTED: CELLULAR BIOLOGY.html'
]

# test there are no bugs with sc html parser
def test_html_parser():
    
    for file_name in TESTFILES:
        file = open(f'{file_name}', 'r')
        print(parse_html(file))

    assert True # just checking for errors, not values
