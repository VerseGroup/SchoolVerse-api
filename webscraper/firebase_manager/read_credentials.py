# python imports
import os
import sys

# adding dir to sys to allow local importing
currentdir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(currentdir)

# firebase imports
import firebase_admin

# local imports
from auth import db

# get user encryptions with id
def get_encrypted_credentials(id, platform_code):
    user_ref = db.collection(u'USERS').document(f'{id}')
    doc = user_ref.get()
    
    if doc.exists:
        doc_dict = doc.to_dict()

        try:
            return {
                "code" : '0',
                "username_ciphertext" : doc_dict[f'{platform_code}_creds'][0],
                "password_ciphertext" : doc_dict[f'{platform_code}_creds'][1]
            }

        except:
            return {
                "message" : "error with reading cipher, probably doesn't exist",
                "code" : "1-a"
            }

    else:
        return {
            "message" : "Invalid user ID",
            "code" : "1a"
        }