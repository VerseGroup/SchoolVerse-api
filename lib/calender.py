from src.webscraper.firebase.events import write_events
from src.webscraper.scraper.veracross import get_events
from src.webscraper.firebase.auth import start_firebase

from getpass import getpass

def scrape_events(db, username, password):
    events = get_events(username, password)
    write_events(events, db)

def script():
    username = input('Username: ')
    password = getpass()

    db = start_firebase()
    scrape_events(db, username, password)

if __name__ == '__main__':
    script()

# add flik next
