# python imports
import os

# firebase imports
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# secrets
from dotenv import load_dotenv
load_dotenv()
FILE_NAME = os.getenv("FILE_NAME")

# authenticate firebase admin SDK
def auth():
    cred = credentials.Certificate(f'SchoolVerse_webscraper/firebase_manager/secrets/{FILE_NAME}')
    firebase_admin.initialize_app(cred)
    db = firestore.client()   
    return db

# variable for other files to import
db = auth()
    
