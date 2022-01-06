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

def write_task(data, user_id):
    check_task_exists(user_id=user_id, platform_information=data['platform_information'])
    id = str(uuid.uuid4())
    db.collection(u'USERS').document(f'{user_id}').collection(u'TASKS').document(f'{id}').set(data)

def check_task_exists(user_id,platform_information):
    tasks_ref = db.collection(u'USERS').document(f'{user_id}').collection(u'TASKS')
    docs = tasks_ref.get()

    for doc in docs:
        doc_dict = doc.to_dict()
        doc_plat_inf = doc_dict['platform_information']
        if doc_plat_inf['assignment_code'] == platform_information['assigment_code'] and doc_plat_inf['code'] == platform_information['code']:
            return True
    
    return False