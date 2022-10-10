# python imports
import os
import uuid
import json

# external imports 
from fastapi import FastAPI
from pydantic import BaseModel
from vgem import EM

# config
from src.config import AUTH_TOKEN_REQUIRED, MAX_EXECUTIONS, ALL_SCHOOL_EVENTS_ICAL, MAX_USER_EXECUTIONS

# clubs
from src.clubs.models import Club, Event, Meeting, Update

# firebase
from src.firebaseV2.auth import start_firebase

# requests
from src.requests import ScrapeRequest, SignUpRequest, CreateClubRequest, JoinClubRequest, EnsureRequest, LeaveClubRequest, UpdateClubRequest, JoinSportRequest, LeaveSportRequest

# webscraper
from src.scraperV2.sc import scrape_schoology, ensure_schoology
from src.scraperV2.vc.events import convert_all_school_events

# firebase
from src.firebaseV2.write import write_key, write_tasks, write_club, write_events, write_menu, write_courses, write_schedule, write_days
from src.firebaseV2.read import get_private_key

# flik
from datetime import date, timezone, datetime, timedelta
from src.scraperV2.fk import scrape_flik
from src.firebaseV2.write import write_menu

# load secrets from .env
from dotenv import load_dotenv
load_dotenv()
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")
TO_EMAIL = os.getenv("TO_EMAIL")

#################################

# startup
app = FastAPI()
db = start_firebase()

# schedules
with open('src/schedules.json', 'r') as f:
    schedules = json.load(f)

# general functions #
def check_user_exists(user_id):
    users = db.collection(u'users').stream()
    for user in users:
        if user.id == user_id:
            return True

def check_club_exists(club_id):
    clubs = db.collection(u'clubs').stream()
    for club in clubs:
        if club.id == club_id:
            return True

def check_sport_exists(sport_id):
    sports = db.collection(u'sports').stream()
    for sport in sports:
        if sport.id == sport_id:
            return True

# execution functions #

executions = 0
USERS_EXECUTIONS = {}

def do_executions():
    # write as a function decorator later

    global executions
    executions += 1
    if executions > MAX_EXECUTIONS:
        return {'message': "error", 'error': f'Too many general executions: {executions}/{MAX_EXECUTIONS}', 'passed': False}
    return {'passed': True}

def do_user_executions(user_id):

    time_now = datetime.now(timezone.utc)
    time_one_day_ago = time_now - timedelta(days=1)
    time_tomorrow = time_now + timedelta(days=1)

    global USERS_EXECUTIONS
    if user_id not in USERS_EXECUTIONS:
        USERS_EXECUTIONS[user_id] = {
            "reset": time_now,
            "executions" : 1
        }
    else:
        reset = USERS_EXECUTIONS[user_id]["reset"]
        if reset < time_one_day_ago:
            USERS_EXECUTIONS[user_id]["reset"] = time_now
            USERS_EXECUTIONS[user_id]["executions"] = 1
        else:
            USERS_EXECUTIONS[user_id]["executions"] += 1
    
    if USERS_EXECUTIONS[user_id]['executions'] > MAX_USER_EXECUTIONS:
        return {'message': "error", 'error': f'Too many user executions today ({time_now.strftime("%m/%d/%Y")}) for user with id [{user_id}]: {USERS_EXECUTIONS[user_id]["executions"]}/{MAX_USER_EXECUTIONS} daily executions. Reset occurs on {time_tomorrow.strftime("%m/%d/%Y")}', 'passed': False}
    return {'passed': True}

def do_flik(db, useToday=True, day=None):
    try:
        if useToday:
            today = datetime.now(timezone.utc)
            today = today.strftime("%d/%m/%Y %H:%M:%S")
            today = today.split(" ")
            the_day = today[0].split('/')

            day = the_day[0]
            month = the_day[1]
            year = the_day[2]

            hour = today[1].split(':')[0]
            if int(hour) + 5 > 24:
                day = str(int(day) + 1)

        menu = scrape_flik(day, month, year)
        
    except Exception as e:
        return {'message': 'failed to scrape flik', 'exception': str(e)}

    try:
        write_menu(menu, db)
    except Exception as e:
        return {'message': 'failed to write to firebase', 'exception': str(e)}

    return {"message": "success"}

####### ROUTES [SCRAPER] #######
@app.post("/getkey", status_code=200)
def get_key(request: SignUpRequest):
    response = do_user_executions(request.user_id)
    if response['passed'] == False:
        return response

    # check user exists
    if not check_user_exists(request.user_id):
        return {"message": "user does not exist"}

    # check if user exists

    if db.collection(u'users').document(f'{request.user_id}').get().exists:
        pass
    else:
        return {"message": "user does not exist"}

    handler = EM()
    private_key = handler.serialize_private_key()
    write_key(private_key, request.user_id, db)
    db.collection(u'users').document(f'{request.user_id}').update({u'task_ids': []})

    public_key = handler.serialize_public_key()
    return {
        "message": "success",
        "public_key": public_key,
    }

@app.post("/scrape", status_code=200)
def scrape(request: ScrapeRequest):
    response = do_user_executions(request.user_id)
    if response['passed'] == False:
        return response

    # check user exists
    if not check_user_exists(request.user_id):
        return {"message": "user does not exist"}

    private_key = get_private_key(request.user_id, db)

    if private_key['message'] != 'success':
        return private_key
    else:
        private_key = private_key['key']
    
    handler = EM(serialized_private_key=private_key)
    username = handler.decrypt_rsa(request.e_username, True)
    password = handler.decrypt_rsa(request.e_password, True)

    try:
        returns = scrape_schoology(username, password)
        tasks = returns['tasks']
    except Exception as e:
        return {"message": "failed to scrape schoology", "exception": str(e)}

    try:
        write_tasks(tasks, request.user_id, db)
    except Exception as e:
        return {"message": "failed to write tasks to firebase", "exception": str(e)}

    return {"message": "success"}

@app.post("/ensure", status_code=200)
def ensure(request: EnsureRequest):
    response = do_user_executions(request.user_id)
    if response['passed'] == False:
        return response

    # check user exists
    if not check_user_exists(request.user_id):
        return {"message": "user does not exist"}

    private_key = get_private_key(request.user_id, db)

    if private_key['message'] != 'success':
        return private_key
    else:
        private_key = private_key['key']
    
    handler = EM(serialized_private_key=private_key)
    username = handler.decrypt_rsa(request.e_username, True)
    password = handler.decrypt_rsa(request.e_password, True)

    result = ensure_schoology(username, password)
    if result == True:
        returns = scrape_schoology(username, password)
        write_courses(returns['courses'], request.user_id, db)

        try:
            email = str(username) + "@students.hackleyschool.org"
            schedule = schedules[email]
        except Exception as e:
            return {"message": "failed to get schedule", "exception": str(e)}

        try:
            write_schedule(schedule, request.user_id, db)
        except Exception as e:
            return {"message": "failed to write schedule to firebase", "exception": str(e)}

        return {"message": "success"}
    else:
        return {"message": "failed to ensure schoology"}

####### ROUTES [ClUBS] #######
@app.post("/club/create", status_code=200)
def create_club(request: CreateClubRequest):
    response = do_executions()
    if response['passed'] == False:
        return response

    club = Club(
        name=request.name,
        description=request.description,
        members=request.leaders,
        leaders = request.leaders,
        meeting_blocks=request.meeting_blocks,
    )
    return write_club(club, db)

@app.post("/club/join", status_code=200)
def join_club(request: JoinClubRequest):
    response = do_user_executions(request.user_id)
    if response['passed'] == False:
        return response

    if not check_user_exists(request.user_id):
        return {"message": "user does not exist"}
    if not check_club_exists(request.club_id):
        return {"message": "club does not exist"}

    club = db.collection(u'clubs').document(f'{request.club_id}').get().to_dict()
    try:
        if request.user_id in club['members']:
            return {"message": "user already in club"}
        club['members'].append(request.user_id)
    except:
        club['members'] = [request.user_id]
    db.collection(u'clubs').document(f'{request.club_id}').update(club)

    user = db.collection(u'users').document(f'{request.user_id}').get().to_dict()
    try:
        if request.club_id not in user['club_ids']:
            user['club_ids'].append(request.club_id)
    except:
        user['clubs'] = [request.club_id]
    db.collection(u'users').document(f'{request.user_id}').update(user)

    return {"message": "success"}

@app.post("/club/leave", status_code=200)
def leave_club(request: LeaveClubRequest):
    response = do_user_executions(request.user_id)
    if response['passed'] == False:
        return response

    if not check_user_exists(request.user_id):
        return {"message": "user does not exist"}
    if not check_club_exists(request.club_id):
        return {"message": "club does not exist"}

    club = db.collection(u'clubs').document(f'{request.club_id}').get().to_dict()
    try:
        if request.user_id in club['members']:
            club['members'].remove(request.user_id)
    except:
        club['members'] = []
    db.collection(u'clubs').document(f'{request.club_id}').update(club)

    user = db.collection(u'users').document(f'{request.user_id}').get().to_dict()
    try:
        if request.club_id in user['club_ids']:
            user['club_ids'].remove(request.club_id)
    except:
        user['clubs'] = []
    db.collection(u'users').document(f'{request.user_id}').update(user)

    return {"message": "success"}

@app.post("/club/update", status_code=200)
def update_club(request: UpdateClubRequest):
    response = do_user_executions(request.user_id)
    if response['passed'] == False:
        return response

    if not check_club_exists(request.club_id):
        return {"message": "club does not exist"}

    if not check_user_exists(request.user_id):
        return {"message": "user does not exist"}

    club = db.collection(u'clubs').document(f'{request.club_id}').get().to_dict()

    if request.user_id not in club['leaders']:
        return {"message": "user is not a leader of the club"}

    club[request.field_to_update] = request.new_value

    db.collection(u'clubs').document(f'{request.club_id}').update(club)

    return {"message": "success"}

####### ROUTES [SPORTS] #######
@app.post("/sport/join", status_code=200)
def join_sport(request: JoinSportRequest):
    response = do_user_executions(request.user_id)
    if response['passed'] == False:
        return response

    if not check_user_exists(request.user_id):
        return {"message": "user does not exist"}

    if not check_sport_exists(request.sport_id):
        return {"message": "sport does not exist"}

    user_dict = db.collection(u'users').document(f'{request.user_id}').get().to_dict()['subscribed_sports']

    try:
        user_sports = user_dict['subscribed_sports']
    except:
        user_sports = []

    if request.sport_id in user_sports:
        return {"message": "user already subscribed to sport"}
    else:
        user_sports.append(request.sport_id)
        db.collection(u'users').document(f'{request.user_id}').update({'subscribed_sports': user_sports})
        return {"message": "success"}

@app.post("/sport/leave", status_code=200)
def leave_sport(request: LeaveSportRequest):
    response = do_user_executions(request.user_id)
    if response['passed'] == False:
        return response

    if not check_user_exists(request.user_id):
        return {"message": "user does not exist"}

    if not check_sport_exists(request.sport_id):
        return {"message": "sport does not exist"}

    user_dict = db.collection(u'users').document(f'{request.user_id}').get().to_dict()
    
    try:
        user_sports = user_dict['subscribed_sports']
    except:
        return {"message": "user not subscribed to sport"}
    
    if request.sport_id not in user_sports:
        return {"message": "user not subscribed to sport"}
    else:
        user_sports.remove(request.sport_id)
        db.collection(u'users').document(f'{request.user_id}').update({'subscribed_sports': user_sports})
        return {"message": "success"} 

####### ROUTES [VERACROSS] #######

@app.get("/events", status_code=200)
def get_events():
    response = do_executions()
    if response['passed'] == False:
        return response

    try:
        days, events = convert_all_school_events(ALL_SCHOOL_EVENTS_ICAL)
    except Exception as e:
        return {"message": "failed to convert all school events", "exception": str(e)}

    try:
        write_events(events, db)
        write_days(days, db)
    except Exception as e:
        return {"message": "failed to write events to firebase", "exception": str(e)}

    return {"message": "success"}

####### ROUTES [FLIK] #######
@app.get("/flik", status_code=200)
def flik():
    response = do_executions()
    if response['passed'] == False:
        return response
    
    return do_flik(db)

####### ROUTES [GENERAL] #######
@app.get("/ping", status_code=200)
async def ping():
    return {"message": "pong"} 

'''
TODO
User's should have cached information if not scraped 
-> cache schedule
-> cache tasks
etc. 
'''