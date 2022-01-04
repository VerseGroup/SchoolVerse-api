# python imports
import os
import sys

# adding dir to sys to allow local importing
currentdir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(currentdir)

# firebase imports
import firebase_admin

# local imports
from .auth import auth

# setting up firebase db
db = auth()

# get user encryptions with id
def get_encrypted_credentials(id, platform_code):
    user_ref = db.collection(u'USERS').document(f'{id}')
    doc = user_ref.get()
    if doc.exists:
        doc_dict = doc.to_dict()
        return {
            "username_ciphertext" : doc_dict['SCHOOLOGY_CREDS'][0],
            "password_ciphertext" : doc_dict['SCHOOLOGY_CREDS'][1]
        }
    else:
        return {
            "message" : "Invalid user ID"
        }