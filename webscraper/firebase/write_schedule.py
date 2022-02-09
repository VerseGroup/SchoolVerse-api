# python imports
import uuid

# firebase imports
import firebase_admin

# local imports
from webscraper.firebase.auth import db

def write_schedule(user_id, schedule, day):
    for period in schedule:
        db.collection(u'USERS').document(f'{user_id}').collection(u"SCHEDULE").document(f'DAY{day}').collection(u"PERIODS").document(f"{period}").set(schedule[period])
