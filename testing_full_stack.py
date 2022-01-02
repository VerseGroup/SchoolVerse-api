# testing following arch.txt pattern
from SchoolVerse_webscraper.scraper import scrape_schoology
from SchoolVerse_webscraper.firebase_manager import get_encrypted_credentials
from SchoolVerse_webscraper.encryption_manager import decrypt

# TESTING USER 
ID = input('ID: ')
KEY = input('DECRYPTION KEY: ')

credentials = get_encrypted_credentials(ID, 'sc')
username = decrypt(credentials['username_ciphertext'], KEY)
password = decrypt(credentials['password_ciphertext'], KEY)

print(scrape_schoology(username, password))