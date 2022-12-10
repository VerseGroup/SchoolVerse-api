# firebase imports
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth
from src.config import MODE

# secrets
if MODE == "dev":
    FILE_NAME = 'testingsdk.json'
else:
    FILE_NAME = 'prodsdk.json'
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
    
def delete_user(user_id):
    auth.delete_user(user_id)