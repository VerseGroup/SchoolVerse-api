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

# writes a task to firebase within a user collection task collection, after checking that it doens't already exist
def write_task(task, user_id):
    platform_information = task['platform_information']
    exists = check_task_exists(user_id=user_id, platform_information=platform_information)
    
    if not exists:
        id = str(uuid.uuid4())
        db.collection(u'USERS').document(f'{user_id}').collection(u'TASKS').document(f'{id}').set(task)

# iterates through connections to make sure it doesn't overwrite existing data
def check_task_exists(user_id, platform_information):
    tasks_ref = db.collection(u'USERS').document(f'{user_id}').collection(u'TASKS')
    docs = tasks_ref.get()

    for doc in docs:
        doc_dict = doc.to_dict()
        print(doc_dict)
        doc_plat_inf = doc_dict['platform_information']
        if doc_plat_inf['assignment_code'] == platform_information['assignment_code'] and doc_plat_inf['platform_code'] == platform_information['assignment_code']:
            return True
    
    return False