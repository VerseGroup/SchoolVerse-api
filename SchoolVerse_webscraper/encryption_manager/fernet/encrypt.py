# for development purposes

# python imports
from getpass import getpass

# external imports
from cryptography.fernet import Fernet

# get creds
#username = input('USERNAME: ')
#password = getpass()

# encrypt creds using fernet
def encrypt(username, password): 
    key = Fernet.generate_key()
    f = Fernet(key)
    username_token = f.encrypt(f'{username}'.encode('utf-8'))
    password_token = f.encrypt(f'{password}'.encode('utf-8'))
    return {
        "username": username_token,
        "password": password_token,
        "key": key
    }

#print(encrypt(username, password))