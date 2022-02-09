# firebase imports
import firebase_admin

# local imports
from webscraper.firebase.auth import db

# get user encryptions with id
def get_encrypted_credentials(id, platform_code) -> dict:
    user_ref = db.collection(u'USERS').document(f'{id}')
    doc = user_ref.get()
    
    if doc.exists:
        doc_dict = doc.to_dict()
        creds = doc_dict['CREDS']

        try:
            return {
                "code" : '0',
                "username_ciphertext" : creds[f'{platform_code}'][0],
                "password_ciphertext" : creds[f'{platform_code}'][1]
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