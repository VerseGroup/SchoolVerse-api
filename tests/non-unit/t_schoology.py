# python imports
import os
import sys
import time

# adding directories for local imports
parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentdir)
currentdir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(currentdir)
tripleparentdir = os.path.abspath(os.path.join(parentdir, os.path.pardir))
sys.path.append(tripleparentdir)

# external imports
from getpass import getpass

# local imports
from webscraper.scraper import scrape_schoology

def test_scraper():
    # loading schoology username/password to test
    username = input('Schoology Username: ')
    password = getpass()

    # testing schoology scraper
    start_time = time.time() # A timer to measure speed
    print()
    print(scrape_schoology(username, password, False))

    # outputting runtime of scraper
    print()
    print(f"Executed in {time.time() - start_time} seconds")
    print()

if __name__ == "__main__":
    test_scraper()
    
