# full test of veracross webscraping

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
from src.scraperV2.vc.vc import scrape_veracross

def test_veracross():
    USERNAME = input('USERNAME: ')
    PASSWORD = getpass()

    start_time = time.time()
    
    days = scrape_veracross(USERNAME, PASSWORD)
    print(days)
    
    print(f"Executed in {time.time() - start_time} seconds\n")

if __name__ == "__main__":
    test_veracross()