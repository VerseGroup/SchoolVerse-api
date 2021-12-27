# testing file to test various functionality

# python imports

# external imports
from getpass import getpass

# local imports
from SchoolVerse_webscraper.scraper.schoology.schoology import scrape_schoology

# loading schoology username/password to test
username = input('Schoology Username: ')
password = getpass()

# testing schoology scraper
print(scrape_schoology(username, password))