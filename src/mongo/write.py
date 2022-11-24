# imports
from asyncio import current_task
import json, uuid
from datetime import datetime, date, time, timedelta


#data base 

def write_courses(courses, user_id, db):
    user_dict = db['users'].find_one({'_id' : user_id})

    user_courses = []

    for course in courses:
        try:
            course = course.serialize()
            del course['section']
        except:
            pass
        user_courses.append(course)

    user_dict['courses'] = user_courses
    
    db['users'].update_one({'_id' : user_id}, {'$set' : {'courses' : user_courses}})




def write_key(private_key, user_id, db):

    # getting the current cred array

    # writing the data to the database
    db['users'].update_one({'_id' : user_id}, {'$set' : {'private_key' : private_key}})


    # old firebase code - out of order
    #db.collection(u'users').document(f'{user_id}').update(formatted_data) 
    # formatting the creds into the dictionary
    #formatted_data = {"private_key" : private_key}
    
    return {"message" : "success"}

# right now it deletes all then writes all, but it should be changed to only write new ones
def write_events(events, db):
    
    #delete events
    db["events"].delete_many({})
    

    for event in events:

        # skipping MS, LS, ADM, and T for now
        if "MS:" in event['summary'] or "LS:" in event['summary'] or "T:" in event['summary'] or "ADM:" in event['summary']:
            continue

        if "MS" in event['summary'] or "LS" in event['summary']:
            continue

        start = event['day']

        # skipping events that are not in the future
        if start < datetime.now(start.tzinfo):
            continue

        # skipping events that are over a two weeks away
        if start > (datetime.now(start.tzinfo) + timedelta(days=14)):
            continue

        # add event for mongodb interpretation
        event['_id'] = event['id']
        event.pop('id')
        db["events"].insert_one(event)

       

def write_days(days, db):
    # redo with list comprehension and insert many
    
    db["days"].delete_many({})
    
    for day in days:
        day['_id'] = day['id']
        day.pop('id')
        db["days"].insert_one(day)

# writes menu to firebase
def write_menu(menu, db):

    

    db['menus'].delete_many({})
    

    for date in menu:
        # convert date to a datetime object
        try: 
            datetime_object = convert_flik_date(date)
        except:
            continue

        # check if date is sat or sunday and skip if it is
        if datetime_object.weekday() == 5 or datetime_object.weekday() == 6:
            continue
        
        # create to write object
        to_write = menu[date]
        to_write['breakfast'] = to_write['breakfast']['food']
        to_write['lunch'] = to_write['lunch']['food']
        to_write['dinner'] = to_write['dinner']['food']
        to_write['date'] = datetime_object
        to_write['_id'] = date

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
            
        # write to database
        db['menus'].insert_one(to_write)
        

# check - this could be renamed for specificity
def check_task_exists(schoology_id, db, user_id):

    user = db['users'].find_one({'_id' : user_id})
    tasks = user.find({})

    for task in tasks:
        if task['platform_information']['assignment_code'] == schoology_id:
            return True
    return False


def write_task(task, user_id, db):
    
    task['due_date'] = convert_date(task['due_date'])
    task['name'] = task['name'].replace('&amp;', '&')
    task['_id'] = uuid.uuid4()
    
    db['users'].update_one({'_id' : user_id}, {'$push' : {'tasks' : task}})

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
        

    club["_id"] = club["id"]
    club.pop("id")
    
    db['clubs'].insert_one(club)

    return {"message" : "success", "club" : club}

# sports

def write_sports(sports, db):

    

    db['sports'].delete_many({})

    for sport in sports:
        
        # skipping MS and Middle School
        if "Middle School" in sport['id'] or "MS." in sport['id']:
            continue

        for event in sport['events']:

            if event['start'] is None:
                try:
                    sport['events'].remove(event)
                except Exception as e:
                    raise Exception(f"could not remove event {str(e)}")
                continue

            event['name'] = sport['name']

            if len(event['name'].split(": ")) == 2:
                event['name'] = event['name'].split(": ")[1]

            if len(event['description'].split(": ")) == 2:
                event['description'] = event['description'].split(": ")[1]

            if len(event['summary'].split(": ")) == 2:

                if 'POSTPONED' in event['summary']:
                    event['summary'] = str("POSTPONED: " + str(event['summary'].split(": ")[1]))
                elif 'CANCELLED' in event['summary']:
                    event['summary'] = str("CANCELLED: " + str(event['summary'].split(": ")[1]))
                else:
                    event['summary'] = event['summary'].split(": ")[1]

        if len(sport['id'].split(": ")) == 2:
                sport['id'] = sport['id'].split(": ")[1]

    for sport in sports:
        good_events = []
        for event in sport['events']:
            try:
                if event['start'] is not None and event['name'] is not None:
                    good_events.append(event)

                if event['name'] is None:
                    event['name'] = sport['name']
                    good_events.append(event)
                    
            except:
                continue
        sport['events'] = good_events
        sport['_id'] = sport["id"]
        sport.pop("id")

        db["sports"].insert_one(sport)

# schedule

def write_schedule(schedule, user_id, db):

    user_ref = db['users'].find_one({'_id' : user_id})

    user_ref.update_one({'_id' : user_id}, {'schedule' : schedule})
    

# # write sc events
# def write_sc_events(events, user_id, db):
#     for event in events:
#         schoology_id = event['platform_information']['assignment_code']
#         if not check_task_exists(schoology_id, db, user_id):
#             write_sc_event(event, user_id, db)
#         else:
#             print(f"Event already exists")

# # write sc event
# def write_sc_event(event, user_id, db):
#     event['due_date'] = convert_date(event['due_date'])
#     event['name'] = event['name'].replace('&amp;', '&')

#     name = event['name']
#     if "Day " in name or "No School" in name:
#         return

#     db.collection(u'users').document(f"{user_id}").collection(u'sc_events').document(f"{uuid.uuid4()}").set(event)
 
