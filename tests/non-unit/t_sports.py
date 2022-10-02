# imports
from getpass import getpass
import os, sys

# adding directories for local imports
parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
doubleparentdir = os.path.abspath(os.path.join(parentdir, os.path.pardir))
sys.path.append(doubleparentdir)

# local imports
from src.scraperV2.vc.icals import get_icals

if __name__ == "__main__":
    username = input("Enter your username: ")
    password = getpass("Enter your password: ")

    icals = get_icals(username, password)

    print(icals)
