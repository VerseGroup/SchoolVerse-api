# python imports
import pyperclip

# local imports
from SchoolVerse_webscraper.encryption_manager.rsa.encryption_handler import EncryptionHandler
from SchoolVerse_webscraper.firebase_manager import write_task, get_encrypted_credentials
from SchoolVerse_webscraper.scraper.schoology import scrape_schoology

# external imports
from getpass import getpass

# copying function
def copy(message, remove_b = False):
    if remove_b:
        message = str(message)[2:-1]
    pyperclip.copy(str(message))

def paste():
    return pyperclip.paste()

def get_encrypted_creds():
    # creds
    username = input('USERNAME: ')
    password = getpass()

    # encryption
    encryption = EncryptionHandler()
    encrypted_username = encryption.encrypt(username, base64_=True)
    encrypted_password = encryption.encrypt(password, base64_=True)

    print(f"USERNAME:{encrypted_username}")
    copy(encrypted_username)
    continue_ = input('')
    
    print(f"PASSWORD:{encrypted_password}")
    copy(encrypted_password)
    continue_ = input('')
    
    private_key = encryption.serialize_private_key()
    return private_key['serialized_private_key']

def scrape_write(key):
    private_key = key
    encryption = EncryptionHandler(serialized_private_key=private_key)

    cred_dict = get_encrypted_credentials('1', 'sc')

    print(cred_dict)

    username = encryption.decrypt(cred_dict['username_ciphertext'], base64_=True)
    password = encryption.decrypt(cred_dict['password_ciphertext'], base64_=True)

    print([username, password])

    '''
    tasks = scrape_schoology(username=username, password=password)  
    print(tasks)

    for task in tasks:
        write_task(task, '1')
    '''

key = get_encrypted_creds()
scrape_write(key)