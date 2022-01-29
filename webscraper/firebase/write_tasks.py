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

def write_tasks(tasks, user_id):
    user_ref = db.collection(u'USERS').document(f'{user_id}')
    user_dict = user_ref.get().to_dict()

    for task in tasks:
        id = task['platform_information']['assignment_code']
        if check_task_exists(id, user_dict):
            print(f"Task {id} already exists")
        else: 
            write_task(task, id, user_id, user_dict)

# writes a task to firebase within a user collection task collection, after checking that it doens't already exist
def write_task(task, id, user_id, user_dict):
    db.collection(u'USERS').document(f'{user_id}').collection(u'TASKS').document(f'{id}').set(task)
    db.collection(u'USERS').document(f'{user_id}').update({"TASK_IDS": user_dict['TASK_IDS'] + [id]})

# iterates through connections to make sure it doesn't overwrite existing data
def check_task_exists(id, user_dict) -> bool:

    if user_dict is not None:
        existingids = user_dict['TASK_IDS']

    for existingid in existingids:
        if existingid == id:
            return True
    
    return False


