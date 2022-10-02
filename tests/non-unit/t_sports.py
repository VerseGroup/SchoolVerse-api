# imports
from getpass import getpass
import os, sys

# adding directories for local imports
parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
doubleparentdir = os.path.abspath(os.path.join(parentdir, os.path.pardir))
sys.path.append(doubleparentdir)

# local imports
from src.scraperV2.vc.icals import get_icals
from src.firebaseV2.write import write_sports
from src.firebaseV2.auth import start_firebase

if __name__ == "__main__":
    db = start_firebase()

    username = input("Enter your username: ")
    password = getpass("Enter your password: ")

    icals = get_icals(username, password)

    sports = {}

    for ical in icals:
        sport = {
            "id" : ical,
            "ical" : icals[ical],
        }
    
    write_sports(icals, db)
