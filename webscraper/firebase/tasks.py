import uuid

def write_tasks(tasks, user_id, db):
    user_ref = db.collection(u'USERS').document(f'{user_id}')

    for task in tasks:
        user_dict = user_ref.get().to_dict()
        schoology_id = task['platform_information']['assignment_code']
        if check_task_exists(schoology_id, user_dict, db):
            print(f"Task {schoology_id} already exists")
        else: 
            write_task(task, schoology_id, user_id, user_dict, db)

# writes a task to firebase within a user collection task collection, after checking that it doens't already exist
def write_task(task, schoology_id, user_id, user_dict, db):
    task = {"task": task}
    task['user_id'] = user_id

    task_uuid = str(uuid.uuid4())
    db.collection(u'TASKS').document(f'{task_uuid}').set(task)

    db.collection(u'USERS').document(f'{user_id}').update({"SCHOOLOGY_TASK_IDS": user_dict['SCHOOLOGY_TASK_IDS'] + [schoology_id]})

# iterates through connections to make sure it doesn't overwrite existing data
def check_task_exists(id, user_dict, db) -> bool:

    if user_dict is not None:
        existingids = user_dict['SCHOOLOGY_TASK_IDS']

    for existingid in existingids:
        if existingid == id:
            return True
    
    return False


