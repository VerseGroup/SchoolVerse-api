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
from auth import auth

# setting up firebase db
db = auth()

def write_task(data, user_id):
    id = str(uuid.uuid4())
    db.collection(u'USERS').document(f'{user_id}').collection(u'TASKS').document(f'{id}').set(data)

