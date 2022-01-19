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

def write_schedule(user_id, schedule):
    db.collection(u'USERS').document('SCHEDULE').set(schedule)