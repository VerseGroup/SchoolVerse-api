# full stack test 
'''
USERNAME + PASSWORD - > VGEM - > FIREBASE
FIREBASE - > SCRAPER - > PARSER -> FIREBASE
'''

# python imports
import os
import sys
import time
import threading 

# adding directories for local imports
parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentdir)
currentdir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(currentdir)
doubleparentdir = os.path.abspath(os.path.join(parentdir, os.path.pardir))
sys.path.append(doubleparentdir)

# local imports
from webscraper.firebase import write_tasks, get_encrypted_credentials, write_creds, write_schedule
from webscraper.scraper.schoology.scraper import scrape_schoology
from webscraper.scraper.veracross.run import scrape_veracross

# external imports
from getpass import getpass
from vgem import EM

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

    write_creds(username=en_username, password=en_password, user_id='1', platform_code='sc')

    return handler.serialize_private_key()

def veracross(username, password):
    scraped_content = scrape_veracross(username, password)
    day = scraped_content[0]
    schedule = scraped_content[1]

    print()
    print(f"DAY : {day}")

    print()
    print(f"SCHEDULE: {schedule}")
    write_schedule(1, schedule, day)

    return "Finished Veracross"

def schoology(username, password):
    tasks = scrape_schoology(username, password)['tasks']
    write_tasks(tasks, 1)

    return "Finished Schoology"

def scrape_using_creds(key):
    handler = EM(serialized_private_key=key)

    cred_dict = get_encrypted_credentials(1, "sc")
    
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

    for thread in threads:
        thread.start()

    for thread in threads:
        response = thread.join()
        print()
        print(response)
        print()

    # threading end #

    print()
    print("FINISHED FULL STACK")  
    print()

def full_stack():
    #start_time = time.time()
    key = get_creds()

    input('Continue? ')

    scraping_start_time = time.time()
    scrape_using_creds(key)

    print()
    #print(f"Executed in {time.time() - start_time} seconds")
    print(f"Scraping Executed in {time.time() - scraping_start_time} seconds")
    print()

if __name__ == '__main__':
    full_stack()
    

