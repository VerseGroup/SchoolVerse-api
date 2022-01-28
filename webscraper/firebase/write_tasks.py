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
    id = task['platform_information']['assignment_code']

    user_ref = db.collection(u'USERS').document(f'{user_id}')
    user_dict = user_ref.get().to_dict()

    exists = check_task_exists(user_id, id, user_dict)
    
    if not exists:
        db.collection(u'USERS').document(f'{user_id}').collection(u'TASKS').document(f'{id}').set(task)
        db.collection(u'USERS').document(f'{user_id}').update({"task_ids": user_dict['task_ids'] + [id]})
    else:
        print(f"Task {id} already exists")

# iterates through connections to make sure it doesn't overwrite existing data
def check_task_exists(id, user_dict):

    if user_dict is not None:
        existingids = user_dict['task_ids']

    for existingid in existingids:
        if existingid == id:
            return True
    
    return False



