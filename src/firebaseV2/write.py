# imports
from src.firebaseV2.utils import convert_date, convert_flik_date
import json, uuid
from datetime import datetime, date, time


def write_courses(courses, user_id, db):
    user_dict = db.collection(u'users').document(f"{user_id}").get().to_dict()

    user_courses = user_dict['COURSES']
    if user_courses is None:
        user_courses = []

    for course in courses:
        course = course.serialize()
        user_courses.append(course)

    user_dict['COURSES'] = user_courses
    db.collection(u'users').document(f"{user_id}").set(user_dict)


def write_key(private_key, user_id, db):

    # getting the current cred array
    user_ref = db.collection(u'users').document(f'{user_id}')
    doc = user_ref.get()
    
    # formatting the creds into the dictionary
    formatted_data = {"private_key" : private_key}

    # writing the data to the database
    db.collection(u'users').document(f'{user_id}').update(formatted_data) 
    
    return {"message" : "success"}

# right now it deletes all then writes all, but it should be changed to only write new ones
def write_events(events, db):

    event_docs = db.collection(u'EVENTS').list_documents()
    for doc in event_docs:
        db.collection(u'EVENTS').document(doc.id).delete()

    for event in events:
        db.collection(u'EVENTS').document(f'{event["id"]}').set(event)

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

def write_schedule(user_id, schedule, db):
    
    schedule = {
        "user_id": str(user_id),
        "schedule": schedule
    }

    # wierd type issue fix
    schedule = json.loads(json.dumps(schedule))

    db.collection(u'SCHEDULES').document(f'{user_id}').set(schedule)

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
def check_task_exists(id, user_dict) -> bool:

    if user_dict is not None:
        existingids = user_dict['task_ids']

    for existingid in existingids:
        if existingid == id:
            return True
    
    return False

def write_tasks(tasks, user_id, db):
    user_ref = db.collection(u'users').document(f'{user_id}').collection(u'tasks')

    for task in tasks:
        user_dict = user_ref.get().to_dict()
        schoology_id = task['platform_information']['assignment_code']
        if check_task_exists(schoology_id, user_dict):
            print(f"Task {schoology_id} already exists")
        else: 
            write_task(task, schoology_id, user_id, user_dict, db)

# writes a task to firebase within a user collection task collection, after checking that it doens't already exist
def write_task(task, schoology_id, user_id, user_dict, db):
    task['user_id'] = user_id
    task['due_date'] = convert_date(task['due_date'])

    task_uuid = str(uuid.uuid4())
    db.collection(u'users').document(f'{user_id}').collection(u'tasks').document(f'{task_uuid}').set(task)

    db.collection(u'users').document(f'{user_id}').update({"task_ids": user_dict['task_ids'] + [schoology_id]})

# clubs

def write_club(club, db):
    club = club.serialize()

    current_clubs = db.collection(u'clubs').list_documents()
    for doc in current_clubs:
        try: 
            if doc.get().to_dict()['name'] == club['name']:
                return {"message" : "club already exists"}
        except:
            pass
        
    db.collection(u'clubs').document(f'{club["id"]}').set(club)

    return {"message" : "success", "club" : club}