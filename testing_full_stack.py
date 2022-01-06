# python imports

# local imports
from SchoolVerse_webscraper.encryption_manager.rsa.encryption_handler import EncryptionHandler
from SchoolVerse_webscraper.firebase_manager import write_task, get_encrypted_credentials
from SchoolVerse_webscraper.scraper.schoology import scrape_schoology

# external imports
from getpass import getpass

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

