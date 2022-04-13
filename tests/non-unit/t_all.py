# full stack test #

# python imports
import os
import sys
import time
import threading 
from datetime import date

# adding directories for local imports
parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
doubleparentdir = os.path.abspath(os.path.join(parentdir, os.path.pardir))
sys.path.append(doubleparentdir)

# firebase imports
from src.webscraper.firebase.credentials import get_encrypted_credentials, write_creds
from src.webscraper.firebase.schedule import write_schedule
from src.webscraper.firebase.tasks import write_tasks
from src.webscraper.firebase.menu import write_menu
from src.webscraper.firebase.courses import write_courses
from src.webscraper.firebase.events import write_events

# scraper imports
from src.webscraper.scraper.schoology.scraper import scrape_schoology
from src.webscraper.scraper.veracross.run import scrape_veracross
from src.webscraper.scraper.flik.scraper import scrape_flik
from src.webscraper.firebase.auth import start_firebase
from src.webscraper.scraper.veracross.events import get_events

# external imports
from getpass import getpass
from vgem import EM

# start firebase instance
db = start_firebase()

# from stack overflow
class ThreadWithReturnValue(threading.Thread):
    def __init__(self, *init_args, **init_kwargs):
        threading.Thread.__init__(self, *init_args, **init_kwargs)
        self._return = None
    def run(self):
        self._return = self._target(*self._args, **self._kwargs)
    def join(self):
        threading.Thread.join(self)
        return self._return

def get_creds():
    username = input('USERNAME: ')
    password = getpass()

    handler = EM()
    en_username = handler.encrypt_rsa(username, True)
    en_password = handler.encrypt_rsa(password, True)

    write_creds(username=en_username, password=en_password, user_id='1', platform_code='sc', db=db)

    return handler.serialize_private_key()

def veracross(username, password):
    days = scrape_veracross(username, password)

    print(f"SCHEDULE: {days}")
    write_schedule(1, days, db)

    return "Finished Veracross"

def events(username, password):
    events = get_events(username, password)
    write_events(events, db)

    return "Finished Events"

def schoology(username, password):
    returns = scrape_schoology(username, password)
    tasks = returns['tasks']
    write_tasks(tasks, 1, db)
    courses = returns['courses']
    write_courses(courses, 1, db)

    return "Finished Schoology"

def flik(today=True):
    if today==True:
        today = date.today()
        today = today.strftime("%d/%m/%Y")
        today = today.split('/')

    menu = scrape_flik(today[0], today[1], today[2])
    write_menu(menu, db)

    return "Finished Flik"

def scrape_using_creds(key):
    handler = EM(serialized_private_key=key)

    cred_dict = get_encrypted_credentials(1, "sc", db)
    
    en_username = cred_dict['username_ciphertext']
    en_password = cred_dict['password_ciphertext']

    username = handler.decrypt_rsa(en_username, True)
    password = handler.decrypt_rsa(en_password, True)

    # threading start #

    threads = []
    t1 = ThreadWithReturnValue(target=schoology, args=(username, password))
    threads.append(t1)
    t2 = ThreadWithReturnValue(target=veracross, args=(username, password))
    threads.append(t2)
    t3 = ThreadWithReturnValue(target=flik)
    threads.append(t3)
    t4 = ThreadWithReturnValue(target=events, args=(username, password))
    threads.append(t4)

    for thread in threads:
        print("\n STARTING THREAD \n")
        thread.start()

    for thread in threads:
        response = thread.join()
        print(f"{response} \n")

        print("CLOSING THREAD \n")
    # threading end #

    print("FINISHED FULL STACK \n")  

def full_stack():
    key = get_creds()

    input('Continue? ')

    scraping_start_time = time.time()
    scrape_using_creds(key)

    print(f"\n Scraping Executed in {time.time() - scraping_start_time} seconds \n")

if __name__ == '__main__':
    full_stack()
    

