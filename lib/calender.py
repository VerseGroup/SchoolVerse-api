from datetime import date

# scraper imports
from src.firebaseV2.write import write_events, write_menu
from src.firebaseV2.auth import start_firebase
#from src.scraperV2.vc.vc import get_events # not finished yet
from src.scraperV2.fk import scrape_flik

# reset imports
from lib.resets.reset_events import reset_events
from lib.resets.reset_flik import reset_flik_tables

from getpass import getpass

def scrape_events(db, username, password):
    events = 1 #get_events(username, password)
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
