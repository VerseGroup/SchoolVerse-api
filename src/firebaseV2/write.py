# imports
from asyncio import current_task
from src.firebaseV2.utils import convert_date, convert_flik_date
import json, uuid
from datetime import datetime, date, time, timedelta

def write_courses(courses, user_id, db):
    user_dict = db.collection(u'users').document(f"{user_id}").get().to_dict()

    user_courses = user_dict['courses']
    if user_courses is None:
        user_courses = []

    for course in courses:
        try:
            course = course.serialize()
        except:
            pass
        user_courses.append(course)

    user_dict['courses'] = user_courses
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
    event_docs = db.collection(u'events').list_documents()
    for doc in event_docs:
        doc.delete()

    for event in events:

        # skipping MS, LS, ADM, and T for now
        if "MS:" in event['summary'] or "LS:" in event['summary'] or "T:" in event['summary'] or "ADM:" in event['summary']:
            continue

        start = event['day']

        # skipping events that are not in the future
        if start < datetime.now(start.tzinfo):
            continue

        # skipping events that are over a two weeks away
        if start > (datetime.now(start.tzinfo) + timedelta(days=14)):
            continue

        db.collection(u'events').document(f'{event["id"]}').set(event)

def write_days(days, db):
    days_docs = db.collection(u'days').list_documents()
    for doc in days_docs:
        doc.delete()

    for day in days:
        db.collection(u'days').document(f'{day["id"]}').set(day)

# writes menu to firebase
def write_menu(menu, db):

    menu_reference = db.collection(u'menus')
    menu_docs = menu_reference.list_documents()

    for doc in menu_docs:
        menu_reference.document(doc.id).delete()

    for date in menu:
        # convert date to a datetime object
        try: 
            datetime_object = convert_flik_date(date)
        except:
            continue

        # check if date is sat or sunday and skip if it is
        if datetime_object.weekday() == 5 or datetime_object.weekday() == 6:
            continue
        
        # write the menu to the database
        menu_ref = db.collection(u'menus').document(date)
        to_write = menu[date]
        to_write['breakfast'] = to_write['breakfast']['food']
        to_write['lunch'] = to_write['lunch']['food']
        to_write['dinner'] = to_write['dinner']['food']
        to_write['date'] = datetime_object

        for meal in to_write:
            if meal == 'date':
                continue

            foods = []
            for food in to_write[meal]:
                name = food['name']
                if name not in foods:
                    foods.append(name)
                else:
                    del to_write[date][meal][food]
            
        menu_ref.set(to_write)

# check
def check_task_exists(schoology_id, db, user_id):

    existing_tasks = db.collection(u'users').document(f"{user_id}").collection(u'tasks').list_documents()

    for doc in existing_tasks:
        if doc.get().to_dict()['platform_information']['assignment_code'] == schoology_id:
            return True
    return False

def write_task(task, user_id, db):
    
    task['due_date'] = convert_date(task['due_date'])
    task['name'] = task['name'].replace('&amp;', '&')

    db.collection(u'users').document(f"{user_id}").collection(u'tasks').document(f"{uuid.uuid4()}").set(task)

# write tasks 
def write_tasks(new_tasks, user_id, db):

    for task in new_tasks:
        schoology_id = task['platform_information']['assignment_code']
        if not check_task_exists(schoology_id, db, user_id):
            write_task(task, user_id, db)
        else:
            print(f"TASK already exists")

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

# sports

def write_sports(sports, db):

    sports_ref = db.collection(u'sports')
    sport_docs = sports_ref.list_documents()

    for doc in sport_docs:
        sports_ref.document(doc.id).delete()

    for sport in sports:
        
        # skipping MS and Middle School
        if "Middle School" in sport['id'] or "MS." in sport['id']:
            continue

        sports_ref.document(f'{sport["id"]}').set(sport)


# schedule

def write_schedule(schedule, user_id, db):

    user_ref = db.collection(u'users').document(f'{user_id}')
    schedule_ref = user_ref.collection(u'schedule').document(f'{user_id}')

    schedule_ref.set(schedule)
    


