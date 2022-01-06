# python imports

# local imports
from SchoolVerse_webscraper.encryption_manager.encryption_handler import EncryptionHandler
from SchoolVerse_webscraper.firebase_manager import write_task, get_encrypted_credentials
from SchoolVerse_webscraper.scraper.schoology import scrape_schoology

# external imports
from getpass import getpass

def get_encrypted_creds():
    # creds
    username = input('USERNAME: ')
    password = getpass()

    # encryption
    encryption = EncryptionHandler()
    encrypted_username = encryption.encrypt(username)
    encrypted_password = encryption.encrypt(password)

    # write directly to firebase
    
    private_key = encryption.serialize_private_key()
    return private_key['serialized_private_key']

def scrape_write(key):
    private_key = key
    encryption = EncryptionHandler(serialized_private_key=private_key)

    cred_dict = get_encrypted_credentials('1', 'sc')

    print(cred_dict)

    username = encryption.decrypt(cred_dict['username_ciphertext'])
    password = encryption.decrypt(cred_dict['password_ciphertext'])

    print([username, password])

    '''
    tasks = scrape_schoology(username=username, password=password)  
    print(tasks)

    for task in tasks:
        write_task(task, '1')
    '''

key = get_encrypted_creds()
scrape_write(key)