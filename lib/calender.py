from datetime import date

# scraper imports
from src.webscraper.firebaseV1.events import write_events
from src.webscraper.scraper.veracross import get_events
from src.webscraper.firebaseV1.auth import start_firebase
from src.webscraper.firebaseV1.menu import write_menu
from src.webscraper.scraper.flik import scrape_flik

# reset imports
from lib.resets.reset_events import reset_events
from lib.resets.reset_flik import reset_flik_tables

from getpass import getpass

def scrape_events(db, username, password):
    events = get_events(username, password)
    write_events(events, db)

def scrape_menus(db, today=True):
    if today==True:
        today = date.today()
        today = today.strftime("%d/%m/%Y")
        today = today.split('/')

    menu = scrape_flik(today[0], today[1], today[2])
    write_menu(menu, db)

def script():
    username = input('Username: ')
    password = getpass()

    db = start_firebase()

    # clearing
    reset_events(db)
    reset_flik_tables(db)

    # filling
    scrape_events(db, username, password)
    scrape_menus(db)

if __name__ == '__main__':
    script()

# add flik next
