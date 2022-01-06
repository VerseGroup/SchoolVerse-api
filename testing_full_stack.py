# python imports

# local imports
from SchoolVerse_webscraper.encryption_manager.rsa.encryption_handler import EncryptionHandler
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

    print(f"USERNAME:{encrypted_username}")
    continue_ = input('')
    print(f"PASSWORD:{encrypted_password}")
    continue_ = input('')
    print(f"PRIVATE_KEY:{encryption.serialize_private_key}")
    continue_ = input('')

def scrape_write():
    private_key = input('PRIVATE_KEY: ')
    encryption = EncryptionHandler(serialized_private_key=private_key)

    cred_dict = get_encrypted_credentials('1', 'sc')
    username = encryption.decrypt(cred_dict['username_ciphertext'])
    password = encryption.decrypt(cred_dict['password_ciphertext'])

    tasks = scrape_schoology(username=username, password=password)  
    print(tasks)

get_encrypted_creds()
input('')
scrape_write()