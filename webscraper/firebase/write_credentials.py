# python imports
import os
import sys
import uuid

# adding dir to sys to allow local importing
currentdir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(currentdir)

# firebase imports
import firebase_admin

# local imports
from auth import db

# writes inputted credential information to firebase (add a platform code parameter in the future)
def write_creds(username, password, user_id, platform_code):
    data = {f"{platform_code}_creds" : [username, password]}
    db.collection(u'USERS').document(f'{user_id}').update(data)