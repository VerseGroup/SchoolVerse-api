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

# writes a task to firebase within a user collection task collection, after checking that it doens't already exist
def write_task(task, user_id):
    platform_information = task['platform_information']
    id = task['platform_information']['assignment_code']

    exists = check_task_exists(user_id, id)
    
    if not exists:
        db.collection(u'USERS').document(f'{user_id}').collection(u'TASKS').document(f'{id}').set(task)
    else:
        print(f"Task {id} already exists")

# iterates through connections to make sure it doesn't overwrite existing data
def check_task_exists(user_id, id):
    tasks_ref = db.collection(u'USERS').document(f'{user_id}').collection(u'TASKS')
    docs = tasks_ref.get()

    for doc in docs:
        if doc.id == id:
            return True
    
    return False



