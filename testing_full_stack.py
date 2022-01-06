# python imports

# local imports
from SchoolVerse_webscraper.encryption_manager.encryption_handler import EncryptionHandler
from SchoolVerse_webscraper.encryption_manager.utils.base64_manager import encode, decode
from SchoolVerse_webscraper.firebase_manager import write_task, get_encrypted_credentials, write_creds
from SchoolVerse_webscraper.scraper.schoology.schoology_scraper import scrape_schoology

# external imports
from getpass import getpass

def get_creds():
    username = input('USERNAME: ')
    password = getpass()

    handler = EncryptionHandler()
    e_username = handler.encrypt(username)
    e_password = handler.encrypt(password)

    en_username = encode(e_username)
    en_password = encode(e_password)

    write_creds(username=en_username, password=en_password, user_id='1')

    return handler.serialize_private_key()

def scrape_using_creds(key):
    handler = EncryptionHandler(serialized_private_key=key)

    cred_dict = get_encrypted_credentials(1, "sc")
    
    en_username = cred_dict['username_ciphertext']
    en_password = cred_dict['password_ciphertext']

    e_username = decode(en_username)
    e_password = decode(en_password)

    username = handler.decrypt(e_username)
    password = handler.decrypt(e_password)

    username = str(username.decode('utf-8'))
    password = str(password.decode('utf-8'))

    all_tasks = scrape_schoology(username, password)
    
    for course in all_tasks:
        course_tasks = all_tasks[course]
        for task in course_tasks:
            write_task(task, 1)

key = get_creds()
input('')
scrape_using_creds(key)

