# python imports
import os
import sys

# adding dir to sys to allow local importing
currentdir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(currentdir)

# firebase imports
import firebase_admin

# local imports
from auth import auth

# setting up firebase db
db = auth()

# get user encryptions with id
def get_encrypted_credentials(id, platform_code):
    users_ref = db.collection(u'USERS')
    docs = users_ref.stream()
    
    for doc in docs:
        if doc.id == id:
            return doc.to_dict()

print(get_encrypted_credentials(1, "sc"))