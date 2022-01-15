'''
# python imports
import os
import sys
import time

# adding directories for local imports
parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentdir)
currentdir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(currentdir)

# external imports
from getpass import getpass

# local imports
from SchoolVerse_webscraper.scraper import scrape_schoology

# loading schoology username/password to test
username = input('Schoology Username: ')
password = getpass()

# testing schoology scraper
start_time = time.time() # A timer to measure speed
print()
print(scrape_schoology(username, password))

# outputting runtime of scraper
print()
print(f"Executed in {time.time() - start_time} seconds")
print()

'''