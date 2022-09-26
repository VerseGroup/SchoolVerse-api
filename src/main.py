# python imports
import os
from turtle import write
import uuid

# external imports 
from fastapi import FastAPI
from pydantic import BaseModel
from vgem import EM

# config
#from src.config import AUTH_TOKEN_REQUIRED

# clubs
from src.clubs.models import Club, Event, Meeting, Update

# firebase
from src.firebaseV2.auth import start_firebase

# requests
from src.requests import ScrapeRequest, SignUpRequest, CreateClubRequest, JoinClubRequest

# webscraper
from src.scraperV2.sc import scrape_schoology, ensure_schoology

# firebase
from src.firebaseV2.write import write_key, write_tasks, write_club
from src.firebaseV2.read import get_private_key

# DELETE LATER !!!!! - TESTING #
def verify_token(token):
    return True

def verify_ios_token(token):
    return True
#################################

# startup
app = FastAPI()
db = start_firebase()

####### ROUTES [SCRAPER] #######
@app.post("/getkey", status_code=200)
def get_key(request: SignUpRequest):
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
        write_tasks(tasks, request.user_id, db)
    except Exception as e:
        return {"message": "failed to scrape schoology", "exception": str(e)}

    return {"message": "success"}

####### ROUTES [ClUBS] #######
@app.post("/club/create", status_code=200)
def create_club(request: CreateClubRequest):
    club = Club(
        name=request.name,
        description=request.description,
        members=request.members,
        leaders = request.leaders,
        meeting_blocks=request.meeting_blocks,
        events=[],
        updates=[],
        meetings=[]
    )
    write_club(club, db)

@app.post("/club/join", status_code=200)
def join_club(request: JoinClubRequest):
    current_members = db.collection(u'clubs').document(f'{request.club_name}').get().to_dict()['members']
    db.collection(u'clubs').document(f'{request.club_name}').update({u'members': current_members.append(request.user_id)})

    current_clubs = db.collection(u'users').document(f'{request.user_id}').get().to_dict()['clubs']
    db.collection(u'users').document(f'{request.user_id}').update({u'clubs': current_clubs.append(request.club_name)})

@app.get("/club/{club_name}", status_code=200)
def get_club(club_name: str):
    club = db.collection(u'clubs').document(f'{club_name}').get().to_dict()
    return club

@app.get("/club/{club_name}/events", status_code=200)
def get_club_events(club_name: str):
    club = db.collection(u'clubs').document(f'{club_name}').get().to_dict()
    return club['events']

@app.get("/club/{club_name}/updates", status_code=200)
def get_club_updates(club_name: str):
    club = db.collection(u'clubs').document(f'{club_name}').get().to_dict()
    return club['updates']

@app.get("/club/{club_name}/meetings", status_code=200)
def get_club_meetings(club_name: str):
    club = db.collection(u'clubs').document(f'{club_name}').get().to_dict()
    return club['meetings']
   
####### ROUTES [GENERAL] #######

@app.get("/ping", status_code=200)
async def ping():
    return {"message": "pong"} 