# python imports
import os
import uuid
import json
import random

# external imports 
from fastapi import FastAPI, Response
from pydantic import BaseModel
from vgem import EM

# config
from src.config import AUTH_TOKEN_REQUIRED, MAX_EXECUTIONS, ALL_SCHOOL_EVENTS_ICAL, MAX_USER_EXECUTIONS, MODE, TESTERS

# steve jobs
from src.stevejobs import STEVEJOBS_SCHEDULE, STEVEJOBS_COURSES, STEVEJOBS_TASKS
stevejobsid = "54fbgGP7RGMAEbkUiMzfKY35tDA3"

# clubs
from src.clubs.models import Club, Event, Meeting, Update

# firebase
from src.firebaseV2.auth import start_firebase

# requests
from src.requests import ScrapeRequest, SignUpRequest, EnsureRequest, ApproveRequest, \
    DeleteUserRequest, NotificationRequest, CreateUserRequest, JoinSportRequest, LeaveSportRequest, \
    CreateClubRequest, JoinClubRequest, LeaveClubRequest

# webscraper
from src.scraperV2.sc import scrape_schoology, ensure_schoology
from src.scraperV2.vc.events import convert_all_school_events, scrape_sport

# firebase
from src.firebaseV2.write import write_key, write_tasks, write_events, write_menu, write_courses, write_schedule, write_days, write_sports#, write_sc_events
from src.firebaseV2.read import get_private_key
from src.firebaseV2.delete_user import delete_user
from src.firebaseV2.create_user import create_user

from src.delete import delete_old_tasks

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
TEST_USER = os.getenv("TEST_USER")
TEST_PASS = os.getenv("TEST_PASS")
NUMBER1 = os.getenv("NUMBER1")
NUMBER2 = os.getenv("NUMBER2")
NUMBER3 = os.getenv("NUMBER3")
NUMBER4 = os.getenv("NUMBER4")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# this is a general API key for all users; make API key user specific later
API_KEY = os.getenv("API_KEY")

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

def check_api_key(api_key):
    if api_key == API_KEY:
        return True
    return False

# execution functions #

server_last_pushed = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=-4))).strftime("%m/%d/%Y %H:%M:%S")

executions = 0
USERS_EXECUTIONS = {}
USER_OPENS = {}
admin_panel_opens = 0
MAX_ADMIN_PANEL_OPENS = 100

def check_admin_panel():
    global admin_panel_opens
    admin_panel_opens += 1
    if admin_panel_opens > MAX_ADMIN_PANEL_OPENS:
        return {'message': "error", 'exception': f'Too many admin panel opens: {admin_panel_opens}/{MAX_ADMIN_PANEL_OPENS}', 'passed': False}
    return {'passed': True}

def do_executions():
    # write as a function decorator later

    global executions
    executions += 1
    if executions > MAX_EXECUTIONS:
        return {'message': "error", 'exception': f'Too many general executions: {executions}/{MAX_EXECUTIONS}', 'passed': False}
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

    if user_id == stevejobsid:
        return {'passed': True}
    
    if USERS_EXECUTIONS[user_id]['executions'] > MAX_USER_EXECUTIONS:
        return {'message': "error", 'exception': f'Too many user executions today ({time_now.strftime("%m/%d/%Y")}) for user with id [{user_id}]: {USERS_EXECUTIONS[user_id]["executions"]}/{MAX_USER_EXECUTIONS} daily executions. Reset occurs on {time_tomorrow.strftime("%m/%d/%Y %H:%M:%S")}.', 'passed': False}
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
        menu2 = scrape_flik(str(int(day)+7), month, year)
        menu = {**menu, **menu2} # combines menu and menu2 (which is one week ahead)
        
    except Exception as e:
        return {'message': 'failed to scrape flik', 'exception': str(e)}

    try:
        write_menu(menu, db)
    except Exception as e:
        return {'message': 'failed to write to firebase', 'exception': str(e)}

    return {"message": "success"}

# user approval #
from src.twilio_client import sendMessage
auth_message_sent = [] # don't want to resend if they spam

####### ROUTES [SCRAPER] #######
@app.post("/getkey", status_code=200)
def get_key(request: SignUpRequest):
    response = do_user_executions(request.user_id)
    if response['passed'] == False:
        return response

    if check_api_key(request.api_key) == False:
        return {'message': "error", 'exception': "invalid api key"}

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

    user_doc = db.collection(u'users').document(f'{request.user_id}').get().to_dict()
    try:
        approved = user_doc['approved']
    except:
        approved = False

    if approved == False:
        db.collection(u'users').document(f'{request.user_id}').update({u'approved': False})

    public_key = handler.serialize_public_key()
    return {
        "message": "success",
        "public_key": public_key,
        "approved": approved
    }

@app.post("/getdata", status_code=200)
def scrape(request: ScrapeRequest):
    response = do_user_executions(request.user_id)
    if response['passed'] == False:
        return response

    if check_api_key(request.api_key) == False:
        return {'message': "error", 'exception': "invalid api key"}

    ### FOR APPLE CHECK ###
    if request.user_id == stevejobsid:
        try:
            return {"message": "success"}
        except Exception as e:
            return {"message": "failed", "exception": str(e)}

    ### FOR APPLE CHECK ###

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
        events = returns['events']

        clean_events = []

        for event in events:
            if not event['course_name'] == 'Upper School':
                clean_events.append(event)

    except Exception as e:
        return {"message": "failed to scrape schoology", "exception": str(e)}

    try:
        write_tasks(tasks, request.user_id, db)
        write_tasks(clean_events, request.user_id, db)
        delete_old_tasks(request.user_id, db) # could another cache table to only delete once a day
    except Exception as e:
        return {"message": "failed to write tasks to firebase", "exception": str(e)}

    return {"message": "success"}

@app.post("/ensure", status_code=200)
def ensure(request: EnsureRequest):
    response = do_user_executions(request.user_id)
    if response['passed'] == False:
        response["message"] = "Too many executions"
        return response

    if check_api_key(request.api_key) == False:
        return {'message': "error", 'exception': "invalid api key"}

    if request.user_id == stevejobsid:
        courses = STEVEJOBS_COURSES
        schedule = STEVEJOBS_SCHEDULE
        try:
            write_courses(courses, request.user_id, db)
            write_schedule(schedule, request.user_id, db)
            return {
                "message": "success"
            }
        except Exception as e:
            return {
                "message": "failed to write stevejobs courses and schedule",
                "exception": str(e)
            }

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
'''
@app.get("/refresh_schedules", status_code=200)
def refresh_schedules():
    users = db.collection(u'users').stream()

    failed = []

    for user in users:
        try:
            the_schedules = db.collection(u'users').document(f'{user.id}').collection(u'schedules').stream()
            for a_schedule in the_schedules:
                db.collection(u'users').document(f'{user.id}').collection(u'schedules').document(f'{a_schedule.id}').delete()

        except Exception as e:
            return {"message": "failed to delete schedules", "exception": str(e)}
        
        try:
            email = str(db.collection(u'users').document(f'{user.id}').get().to_dict()['email'])
            schedule = schedules[email]
        except Exception as e:
            failed.append(str(e))
            continue

        try:
            write_schedule(schedule, str(user.id), db)
        except Exception as e:
            return {"message": "failed to write schedule to firebase", "exception": str(e)}

    return {"message": "success", "failed": failed} 
'''

####### ROUTES [ClUBS] #######

@app.post("/club/create", status_code=200)
def create_club(request: CreateClubRequest):

    clubs = db.collection(u'clubs').stream()
    for club in clubs:
        if club.name == request.name:
            return {"message": "club already exists"}
    
    club = Club(
        id=str(uuid.uuid4()),
        name=request.name,
        description=request.description,
        leader_ids=request.leader_ids,
        member_ids=[],
        meeting_blocks=request.meeting_blocks,
        meeting_block_style = request.meeting_block_style,
        group_notice="",
        status=False,
    )

    db.collection(u'clubs').document(f'{club.id}').set(club.serialize())
    
    # add club to each leader's club list in their user document

    return {"message": "success"}


@app.post("/club/join", status_code=200)
def join_club(request: JoinClubRequest):

    if not check_user_exists(request.member_id):
        return {"message": "user does not exist"}
    if not check_club_exists(request.club_id):
        return {"message": "club does not exist"}

    club = db.collection(u'clubs').document(f'{request.club_id}').get().to_dict()
    if request.member_id in club['member_ids']:
        return {"message": "user already in club"}
    club['member_ids'].append(request.member_id)

    db.collection(u'clubs').document(f'{request.club_id}').update(club)

    user = db.collection(u'users').document(f'{request.member_id}').get().to_dict()
    try:
        if request.club_id not in user['club_ids']:
            user['club_ids'].append(request.club_id)
    except:
        user['club_ids'] = [request.club_id]
    db.collection(u'users').document(f'{request.member_id}').update(user)

    return {"message": "success"}

@app.post("/club/leave", status_code=200)
def leave_club(request: LeaveClubRequest):

    if not check_user_exists(request.member_id):
        return {"message": "user does not exist"}
    if not check_club_exists(request.club_id):
        return {"message": "club does not exist"}

    club = db.collection(u'clubs').document(f'{request.club_id}').get().to_dict()
    
    if request.member_id in club['member_ids']:
        club['member_ids'].remove(request.member_id)
    else:
        return {"message": "user not in club"}

    db.collection(u'clubs').document(f'{request.club_id}').update(club)

    user = db.collection(u'users').document(f'{request.member_id}').get().to_dict()
    try:
        if request.club_id in user['club_ids']:
            user['club_ids'].remove(request.club_id)
    except:
        user['club_ids'] = []
    db.collection(u'users').document(f'{request.member_id}').update(user)

    return {"message": "success"}

####### ROUTES [SPORTS] #######
@app.post("/sport/join", status_code=200)
def join_sport(request: JoinSportRequest):
    response = do_user_executions(request.user_id)
    if response['passed'] == False:
        return response

    if not check_user_exists(request.user_id):
        return {"message": "failed", "exception": "user does not exist"}

    if not check_sport_exists(request.sport_id):
        return {"message:": "failed", "exception": "sport does not exist"}

    user_dict = db.collection(u'users').document(f'{request.user_id}').get().to_dict()

    try:
        user_sports = user_dict['subscribed_sports']
    except:
        user_sports = []

    if request.sport_id in user_sports:
        return {"message": "failed", "exception" : "user already subscribed to sport"}
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
        return {"message" : "failed", "exception": "user does not exist"}

    if not check_sport_exists(request.sport_id):
        return {"message": "failed", "exception" : "sport does not exist"}

    user_dict = db.collection(u'users').document(f'{request.user_id}').get().to_dict()
    
    try:
        user_sports = user_dict['subscribed_sports']
    except:
        return {"message": "failed", "exception" : "user not subscribed to sport"}
    
    if request.sport_id not in user_sports:
        return {"message": "failed", "exception" : "user not subscribed to sport"}
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

@app.get("/sports", status_code=200)
def get_sports():
    response = do_executions()
    if response['passed'] == False:
        return response

    try:
        sports = scrape_sport()
    except Exception as e:
        return {"message": "failed to convert sports", "exception": str(e)}

    try:
        write_sports(sports, db)
    except Exception as e:
        return {"message": "failed to write sports to firebase", "exception": str(e)}

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

@app.get("/version", status_code=200)
async def version():
    return {"ios_version": ['1.2.1', '1.2.2']}

@app.get("/version2", status_code=200)
async def version2():
    return {"ios_version": ['1.2.1', '1.2.2']}

@app.get("/getexecutions", status_code=200)
async def get_executions():
    return USERS_EXECUTIONS

@app.post("/approve", status_code=200)
async def get_approved(request: ApproveRequest):

    if request.user_id not in USER_OPENS:
        USER_OPENS[request.user_id] = 1
    else:
        USER_OPENS[request.user_id] += 1

    if check_api_key(request.api_key) == False:
        return {'message': "error", 'exception': "invalid api key"}
    
    try:
        user_doc = db.collection(u'users').document(f'{request.user_id}').get().to_dict()
    except:
        return {"message": "error", "exception": "user does not exist"}
    
    try:
        approved = user_doc['approved']
    except:
        approved = False
        try:
            db.collection(u'users').document(f'{request.user_id}').update({'approved': False})
        except:
            return {"message": "error", "exception": "failed to assign approved status"}
        
    if approved == False:
        print("FAILED: approved for user " + user_doc['display_name'] + " (" + user_doc['email'] + ")")
        try:
            if user_doc['user_id'] not in auth_message_sent:
                name = user_doc['display_name']
                grade = user_doc['grade_level']
                email = user_doc['email']

                body = f"User {name} ({grade}th grade) -- {email} -- is requesting approval."

                if MODE != "dev":
                    sendMessage(body, NUMBER1)
                    sendMessage(body, NUMBER2)
                    sendMessage(body, NUMBER3)
                    sendMessage(body, NUMBER4)

                auth_message_sent.append(user_doc['user_id'])
        except Exception as e:
            print("failed to send message with error: " + str(e))

    print("approved for user " + user_doc['display_name'] + " (" + user_doc['email'] + ")")
    return {"message": "success","approved": approved}

# NOT GOOD CODE - this is temporary for preparing for presentation day - soon to be a django admin page on a separate server
@app.get("/admin/{password}", status_code=200)
async def admin(password: str):

    response = check_admin_panel()
    if response['passed'] == False:
        return response

    if password == ADMIN_PASSWORD:

        unapproved_users = {}
        all_users = db.collection(u'users').stream()
                   
        if MODE == "dev":
            db_name = "schoolverse-testing-olnqm" 
        else:
            db_name = "schoolverse-5twpt"

        user_ref = db.collection(u'users')
        docs = user_ref.stream()
        for user in docs:
            user_dict = user.to_dict()
            if user_dict['approved'] == False:
                approve_link = f"https://{db_name}.ondigitalocean.app/admin/{ADMIN_PASSWORD}/approve/{user_dict['user_id']}/true"
                unapproved_users[user_dict['user_id']] = [user_dict['display_name'], approve_link, user_dict['grade_level'], user_dict['email']]
     
        html = '''<html>
        <head>
        <title>SV Admin</title>
        <style>
        body {
            font-family: "HelveticaNeue-Bold", "Helvetica Neue Bold", "Helvetica Neue", Helvetica, Arial, "Lucida Grande", sans-serif;
            text-align: center;
            margin: 0;
            height: 100vh;
            background-color: black;
            text-align: center;
        }
        p, a, h1, h2, h3, h4, h5, h6, small {
            color: white;
        }
        h1 {
            font-size: 50px;
        }
        p, a, small, tr, th, td {
            font-family: "HelveticaNeue-Light", "Helvetica Neue Light", "Helvetica Neue", Helvetica, Arial, "Lucida Grande", sans-serif;
        }
        h1, h2, h3, h4, h5, h6 {
            font-family: "HelveticaNeue-Bold", "Helvetica Neue Bold", "Helvetica Neue", Helvetica, Arial, "Lucida Grande", sans-serif;
        }
        h2 {
            font-size: 30px;
        }
        th, td {
            padding: 15px;
            text-align: left;
        }
        th, td {
            margin-bottom: 1px;
        }
        /*
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        tr:nth-child(odd) {
            background-color: grey;
        }
        */
        tr {
            color: white;
        }
        th {
            color: white;
        }
        /* 
        tr:hover {
            background-color: white;
        }
        */
        table {
            margin-left: auto;
            margin-right: auto;
            background-color: black;
            border: 1px solid white;
            border-radius: 10px;
        }
        .server-status-box {
            padding: 20px;
            margin-left: auto;
            margin-right: auto;
            border: 1px solid white;
            border-radius: 10px;
            width: 50%;
            background-color: black;
        }
        .status-text {
            color: green;
        }
        .table-link {
            color: white;
            text-decoration: None;
        }
        .table-link:hover {
            color: green;
        }
        .table-link:active {
            color: red;
        }
        .status-red {
            color: red;
        }
        </style>
        </head>
        '''
        html += f'''
        <body>
        <h1>SchoolVerse Admin Panel</h1>
        <h3> Notes: </h3>
        <small> Welcome, VerseGroup admin. </small>
        <br>
        <small> If you are not a VerseGroup admin, please to not use this service. </small>
        <br>
        <small> Don't spam refresh this page (reads) and don't share this link with anyone. </small>
        <br>
        <small> <a href="https://{db_name}.ondigitalocean.app/docs"> Docs? </a> </small>
        <br>
        <br>
        <small> Your last admin page refresh: <div class="status-text"> {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")} </div> </small>
        <br>
        <h3> Server Status: </h3>
        <div class="server-status-box">
        <p> Server mode: <div class="status-text"> \'{'Production' if MODE == 'prod' else 'Development'}\'  </div> </p>
        <p> Server most recent deployment (last reset date): <div class="status-text"> {server_last_pushed}  </div> </p>
        <p> Admin panel uses: <div class="status-text"> {admin_panel_opens} / {MAX_ADMIN_PANEL_OPENS} </div> </p>
        <p> Current max user scrapes: <div class="status-text"> {MAX_USER_EXECUTIONS} </div> </p>
        <p> Current school-wide scraper uses: <div class="status-text"> {MAX_EXECUTIONS} </div> </p>
        <p> Limit total users : <div class="status-text"> 25 </div> </p>
        </div>
        <h3> Scripts: </h3>
        <div class="server-status-box">
        <p> <a class="table-link" href="/sports"> Sports </a> </p>
        <p> <a class="table-link" href="/events"> Events </a> </p>
        <p> <a class="table-link" href="/flik"> Menus </a> </p>
        </div>
        <h2>Unapproved Users</h2>
        <table>
        <tr>
            <th>Name</th>
            <th>Email</th> 
            <th>Grade</th>
            <th>Approve?</th>
        </tr>
        '''
        unapproved_user_count = 0
        for user_id in unapproved_users:
            unapproved_user_count += 1
            name = unapproved_users[user_id][0]
            grade = unapproved_users[user_id][2]
            email = unapproved_users[user_id][3]
            link = unapproved_users[user_id][1]
            link_button = f"<a class='table-link' href='{link}'>Approve</a>"
            html += f'''
            <tr>
                <td> {name} </td>
                <td> {email} </td>
                <td> {grade} </td>
                <td> {link_button} </td>
            </tr>
            '''
        html += f'''
        </table> <p> Total unapproved users: <div class="status-text"> {unapproved_user_count} </div> </p> <h2>All Users</h2>
        <table>
        <tr>
            <th>Name</th>
            <th>Email</th> 
            <th>Grade</th>
            <th>Approved</th>
            <th>Linked</th>
            <th>Scrapes</th>
            <th>Scrapes Reset</th>
            <th>Launches </th>
            <th>Disapprove</th>
            <th>Reset Scrapes</th>
        </tr>
        '''
        user_count = 0
        for user in all_users:
            user_count += 1
            user_dict = user.to_dict()
            name = user_dict['display_name']
            grade = user_dict['grade_level']
            email = user_dict['email']
            approved = user_dict['approved']
            try:
                private_key = user_dict['private_key']
            except:
                private_key = None
            if private_key == '':
                private_key = None

            if private_key is not None:
                linked = True
            else:
                linked = False

            del private_key # security purposes
            
            remove_link = f"https://{db_name}.ondigitalocean.app/admin/{ADMIN_PASSWORD}/approve/{user_dict['user_id']}/false"
            reset_link = f"https://{db_name}.ondigitalocean.app/admin/{ADMIN_PASSWORD}/reset/{user_dict['user_id']}"
    

            try: 
                executions = USERS_EXECUTIONS[user_dict['user_id']]['executions']
                reset = USERS_EXECUTIONS[user_dict['user_id']]['reset'].strftime("%m/%d/%Y, %H:%M:%S")
                reset = datetime.strptime(reset, "%m/%d/%Y, %H:%M:%S") - timedelta(hours=4) + timedelta(days=1)
            except:
                executions = 0
                reset = "N/A"

            try:
                opens = USER_OPENS[user_dict['user_id']]
            except:
                opens = 0
            html += f'''
            <tr>
                <td> {name} </td>
                <td> {email} </td>
                <td> {grade} </td>
                <td class="{"" if approved == True else "status-red"}"> {approved} </td>
                <td class="{"" if linked == True else "status-red"}"> {linked} </td>
                <td class="{"" if executions == 0 else "status-text"}"> {executions} </td>
                <td class="{"" if reset == "N/A" else "status-text"}"> {reset} </td>
                <td class="{"" if opens == 0 else "status-text"}"> {opens} </td>
                <td> <a class="table-link" href='{remove_link}'>Disapprove?</a> </td>
                <td> <a class="table-link" href='{reset_link}'>Reset Scrapes?</a> </td>
            </tr>
            '''
        html += f"</table><p>Current total users: <div class='status-text'> {user_count} </div> <br> "
        html += f'''
        <table>
        <tr>
            <th>Name</th>
            <th>Rank</th>
        </tr>
        '''
        count = 0
        for tester in TESTERS:
            html += f'''
            <tr>
                <td> {tester} </td>
                <td> {count} </td>
            </tr>
            '''
            count+=1
        html += f"</table><p>Current total testers: <div class='status-text'> {count} </div>"
        html += f"<br> <br> <br> </p> <small> Copyright 2022 VerseGroup, LLC </small> <br> <small> <a href='https://versegroup.tech/privacy'>Privacy Policy?</a></small> <br> <br> </body></html>"
        return Response(content=html, status_code=200)
    else:
        return {"detail": "not found"}

@app.get("/admin/{password}/approve/{user_id}/{approve}", status_code=200)
async def admin_approve(password: str, user_id: str, approve: str):

    response = check_admin_panel()
    if response['passed'] == False:
        return response

    if password == ADMIN_PASSWORD:
                  
        if MODE == "dev":
            db_name = "schoolverse-testing-olnqm" 
        else:
            db_name = "schoolverse-5twpt"

        try:
            db.collection(u'users').document(f'{user_id}').update({'approved': True if approve == "true" else False})
            data = f'''
            <html>
            <head>
            <title>Admin</title>
            </head>
            <body>
            <h1>Success</h1>
            <p>User has been {"approved" if approve == "true" else "disapproved"}</p>
            <p><a href="https://{db_name}.ondigitalocean.app/admin/{ADMIN_PASSWORD}">Back to Admin</a></p>
            </body>
            </html>
            '''
            return Response(content=data, status_code=200)
        except:
            return {"message": "failed", "exception": "user does not exist"}
    else:
        return {"message": "failed"}
    
'''
User's should have cached information if not scraped 
-> cache schedule
-> cache tasks
etc. 
'''

'''
@app.get("/test", status_code=200)
async def test():
    try:
        tasks = []
        steven_ref = db.collection(u'users').document(u'nLakB1MLiJTZjDz8l6bqkT9GpFu2')
        for doc in steven_ref.collection(u'tasks').stream():
            tasks.append(doc.to_dict())

        steven_doc = steven_ref.get().to_dict()
        courses = steven_doc['courses']

        schedule = steven_ref.collection(u'schedule').document(u'nLakB1MLiJTZjDz8l6bqkT9GpFu2').get().to_dict()

        return {
            "tasks": tasks,
            "courses": courses,
            "schedule": schedule
        }
    except Exception as e:
        return {"message": "failed", "exception": str(e)}
'''

@app.get("/admin/{password}/reset/{user_id}", status_code=200)
async def admin_reset(password: str, user_id: str):
    
        response = check_admin_panel()
        if response['passed'] == False:
            return response
    
        if password == ADMIN_PASSWORD:

                        
            if MODE == "dev":
                db_name = "schoolverse-testing-olnqm" 
            else:
                db_name = "schoolverse-5twpt"

            try:
                del USERS_EXECUTIONS[user_id]
                data = f'''
                <html>
                <head>
                <title>Admin</title>
                </head>
                <body>
                <h1>Success</h1>
                <p>User's scrapes have been reset</p>
                <p><a href="https://{db_name}.ondigitalocean.app/admin/{ADMIN_PASSWORD}">Back to Admin</a></p>
                </body>
                </html>
                '''
                return Response(content=data, status_code=200)
            except:
                return {"message": "failed", "exception": "user does not exist"}
        else:
            return {"message": "failed"}
    
@app.post("/create_user", status_code=200)
async def create_user_(request: CreateUserRequest):

    grade_level = int(request.grade_level) # grade level comes in as a stringq

    if check_api_key(request.api_key) == False:
        return {'message': "error", 'exception': "invalid api key"}

    response = create_user(db, request.user_id, request.email, request.display_name, grade_level)
    if response[0]:
        return {"message": "success"}
    else:
        return {"message": "error", "exception": f"{response[1]}"}

@app.post("/delete_user", status_code=200)
async def delete_user_(request: DeleteUserRequest):
    
        if check_api_key(request.api_key) == False:
            return {'message': "error", 'exception': "invalid api key"}
        
        try:
            delete_user(db, request.user_id)
            return {"message": "success"}

        except Exception as e:
            return {"message": "error", "exception": f"{e}"}

@app.get("/notification")
async def notification(request: NotificationRequest):
    if check_api_key(request.api_key) == False:
        return {'message': "error", 'exception': "invalid"}

    return {"message": "success", 
    "notification":
    {
        "title:" : "Welcome to SchoolVerse!",
        "body": "We are excited to have you on board. We hope you enjoy using our app.",
        "link": "https://schoolverse.app",
    }
    }

# iterate through all users and add a subscribed_sports field
@app.get("/add_subscribed_sports")
async def add_subscribed_sports():
    for doc in db.collection(u'users').stream():
        doc.reference.update({'subscribed_sports': []})
    return {"message": "success"}

