# python imports
import os
import sys

# adding directories for local imports
parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentdir)
currentdir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(currentdir)
doubleparentdir = os.path.abspath(os.path.join(parentdir, os.path.pardir))
sys.path.append(doubleparentdir)

# local imports
from vgem.em import EM
from webscraper.firebase_manager import write_task, get_encrypted_credentials, write_creds
from webscraper.scraper.schoology.schoology_scraper import scrape_schoology

# external imports
from getpass import getpass
from vgem.em import EM

def get_creds():
    username = input('USERNAME: ')
    password = getpass()

    handler = EM()
    en_username = handler.encrypt_rsa(username, True)
    en_password = handler.encrypt_rsa(password, True)

    write_creds(username=en_username, password=en_password, user_id='1')

    return handler.serialize_private_key()

def scrape_using_creds(key):
    handler = EM(serialized_private_key=key)

    cred_dict = get_encrypted_credentials(1, "sc")
    
    en_username = cred_dict['username_ciphertext']
    en_password = cred_dict['password_ciphertext']

    username = handler.decrypt_rsa(en_username, True)
    password = handler.decrypt_rsa(en_password, True)

    all_tasks = scrape_schoology(username, password)

    print(all_tasks)

    task_log = open('logs/tasks.txt', 'w')
    for task in all_tasks:
        task_log.write(str(task))
        for tasks in task:
            task_log.write(tasks)
            task_log.write('\n')

        task_log.write('\n\n')
    task_log.close()
    
    
    for course in all_tasks:

        course_tasks = all_tasks[course]
        for task in course_tasks:
            write_task(task, 1)
    

key = get_creds()
input('')
scrape_using_creds(key)

