# testing file to test various functionality

# python imports
import time

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