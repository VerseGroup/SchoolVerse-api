""" # firebase imports
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# secrets
FILE_NAME = 'testing-edacb-firebase-adminsdk-v8h2i-f189331af9.json'
SECRETS_PATH = f'secrets/{FILE_NAME}'

class Firebase:
    def __init__(self):
        
        def auth():
            cred = credentials.Certificate(SECRETS_PATH)
            firebase_admin.initialize_app(cred)
            db = firestore.client()   
            return db
        self.db = auth()

    def get_db(self):
        return self.db

def start_firebase():
    firebase = Firebase()
    return firebase.get_db()
    
 """