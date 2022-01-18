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
from webscraper.firebase_manager import write_task, get_encrypted_credentials, write_creds
from webscraper.scraper.schoology.schoology_scraper import scrape_schoology

# external imports
from getpass import getpass
from vgem import EM

def get_creds():
    username = input('USERNAME: ')
    password = getpass()

    handler = EM()
    en_username = handler.encrypt_rsa(username, True)
    en_password = handler.encrypt_rsa(password, True)

    write_creds(username=en_username, password=en_password, user_id='1', platform_code='sc')

    return handler.serialize_private_key()

def scrape_using_creds(key):
    handler = EM(serialized_private_key=key)

    cred_dict = get_encrypted_credentials(1, "sc")
    
    en_username = cred_dict['username_ciphertext']
    en_password = cred_dict['password_ciphertext']

    username = handler.decrypt_rsa(en_username, True)
    password = handler.decrypt_rsa(en_password, True)

    tasks = scrape_schoology(username, password)
    
    for task in tasks:
        write_task(task, 1)

def full_stack():
    key = get_creds()
    input('')
    scrape_using_creds(key)

if __name__ == '__main__':
    full_stack()
    

