def write_courses(courses, user_id, db):
    user_dict = db.collection(u'USERS').document(f"{user_id}").get().to_dict()

    user_courses = user_dict['COURSES']
    if user_courses is None:
        user_courses = []

    for course in courses:
        course = course.serialize()
        user_courses.append(course)

    user_dict['COURSES'] = user_courses
    db.collection(u'USERS').document(f"{user_id}").set(user_dict)


def write_creds(username, password, user_id, platform_code, db):

    # getting the current cred array
    user_ref = db.collection(u'USERS').document(f'{user_id}')
    doc = user_ref.get()
    
    # if it exists, update the array
    if doc.exists:
        doc_dict = doc.to_dict()
        creds = doc_dict['CREDS']
        creds[f'{platform_code}'] = [username, password]
    
    # if it doesnt exist, create the array
    else:
        creds = {f"{platform_code}" : [username, password]}

    # formatting the creds into the dictionary
    formatted_data = {"CREDS" : creds}

    # writing the data to the database
    db.collection(u'USERS').document(f'{user_id}').update(formatted_data) 
    
    return {"message" : "success"}

from datetime import datetime

def write_events(events, db):
    for event in events:
        write_event(event, db)

def write_event(event, db):
    if check_event_exists(event, db) == False:
        doc_name = f"{event['id']}"
        
        try:
            start = convert_date(event['start_date'], event['start_time'])
            end = convert_date(event['end_date'], event['end_time'])
        except Exception as e:
            start = f"something broke with error {str(e)}"
            end = f"something broke with error {str(e)}"

        event.pop('start_date')
        event.pop('start_time')
        event.pop('end_date')
        event.pop('end_time')
        
        event['start'] = start
        event['end'] = end

        if "Day" in event['description'] and len(event['description']) == 5:
            event.pop('location')
            event.pop('end')
            event.pop('description')
            event['day'] = event['name']
            event.pop('name')
            event['date'] = event['start']
            event.pop('start')

            db.collection(u'DAYS').document(doc_name).set(event)

        else:
            db.collection(u'EVENTS').document(doc_name).set(event)
        
        existing_events = db.collection(u'EVENTS').document('EXISTING_EVENTS').get().to_dict()['EVENTS']

        if existing_events is None:
            existing_events = [event['platform_information']['event_id']]
        else:
            existing_events.append(event['platform_information']['event_id'])
        
        db.collection(u'EVENTS').document("EXISTING_EVENTS").set({"EVENTS": existing_events})
    else:
        print(f"Event {event['id']} already exists")

def check_event_exists(event, db):
    existing_events_dict = db.collection(u'EVENTS').document('EXISTING_EVENTS').get().to_dict()
    existing_events = existing_events_dict['EVENTS']
    if existing_events is not None:
        if event['platform_information']['event_id'] in existing_events:
            return True
    return False

from datetime import datetime

# writes menu to firebase
def write_menu(menu, db):

    menu_reference = db.collection(u'MENUS')
    menu_docs = menu_reference.list_documents()
    for doc in menu_docs:
        menu_reference.document(doc.id).delete()

    for key in menu:
        date = key
        menu_ref = db.collection(u'MENUS').document(date)
        to_write = menu[key]
        to_write['breakfast'] = to_write['breakfast']['food']
        to_write['lunch'] = to_write['lunch']['food']
        to_write['dinner'] = to_write['dinner']['food']
        to_write['date'] = convert_flik_date(date)
        menu_ref.set(to_write)

import json

def write_schedule(user_id, days, db):
    
    schedule = {
        "user_id": str(user_id),
        "days": days
    }

    # wierd type issue fix
    schedule = json.loads(json.dumps(schedule))

    db.collection(u'SCHEDULES').document(f'{user_id}').set(schedule)

# TODO: CLEAN THIS CODE 

from datetime import datetime

def write_sports(events, db):
    for event in events:
        write_sport(event, db)

def write_sport(event, db):
    if check_sports_event_exists(event, db) == False:
        doc_name = f"{event['id']}"

        db.collection(u'SPORTS').document(doc_name).set(event)
        
        existing_events = db.collection(u'SPORTS').document('EXISTING_SPORTS').get().to_dict()['SPORTS']

        if existing_events is None:
            existing_events = [event['platform_information']['id']]
        else:
            existing_events.append(event['platform_information']['id'])
        
        db.collection(u'SPORTS').document("EXISTING_SPORTS").set({"SPORTS": existing_events})
    else:
        print(f"SPORT {event['id']} already exists")

def check_sports_event_exists(event, db):
    existing_events_dict = db.collection(u'SPORTS').document('EXISTING_SPORTS').get().to_dict()
    existing_events = existing_events_dict['SPORTS']
    if existing_events is not None:
        if event['platform_information']['id'] in existing_events:
            return True
    return False

# iterates through connections to make sure it doesn't overwrite existing data
def check_task_exists(id, user_dict, db) -> bool:

    if user_dict is not None:
        existingids = user_dict['SCHOOLOGY_TASK_IDS']

    for existingid in existingids:
        if existingid == id:
            return True
    
    return False

import uuid
from datetime import datetime, date, time

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
    task['user_id'] = user_id
    task['due_date'] = convert_sc_date(task['due_date'])

    task_uuid = str(uuid.uuid4())
    db.collection(u'TASKS').document(f'{task_uuid}').set(task)

    db.collection(u'USERS').document(f'{user_id}').update({"SCHOOLOGY_TASK_IDS": user_dict['SCHOOLOGY_TASK_IDS'] + [schoology_id]})