# python imports
import os

# firebase imports
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# secrets
FILE_NAME = 'testing-edacb-firebase-adminsdk-v8h2i-f189331af9.json'
SECRETS_PATH = f'secrets/{FILE_NAME}'

# authenticate firebase admin SDK
def auth():
    cred = credentials.Certificate(SECRETS_PATH)
    firebase_admin.initialize_app(cred)
    db = firestore.client()   
    return db

# variable for other files to import
db = auth()
    
