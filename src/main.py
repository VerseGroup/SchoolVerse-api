# python imports
import os
import uuid

# external imports 
from fastapi import FastAPI
from pydantic import BaseModel
from vgem import EM

# config
from src.config import AUTH_TOKEN_REQUIRED, SUPPORTED_PLATFORMS

# firebase
from src.firebaseV2.auth import start_firebase
from src.postgres.crud import Backend_Interface

# requests
from src.requests import ScrapeRequest, LinkRequest, SignUpRequest

# webscraper
from src.scraperV2.vc.vc import scrape_veracross
from src.scraperV2.sc import scrape_schoology
from src.scraperV2.fk import scrape_flik

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

@app.post("/scrape", status_code=200)
async def scrape_(request: ScrapeRequest):

    # verify token
    token = request.auth_token
    if AUTH_TOKEN_REQUIRED and not verify_token(db, request.user_id, token):
        return {"error": "Invalid token"}

    # check platform code
    if request.platform_code not in SUPPORTED_PLATFORMS:
        return {"error": "unsupported platform code"}

    ss = Backend_Interface()
    try:
        if request.platform_code == 'sc':
            return False #schoology(db, ss, request.user_id)
        else:
            return {"message": "unsupported platform code"}
    except Exception as e:
        e = str(e).replace('\'','-')
        return {"message": "error", "exception": str(e)}

@app.post("/menu", status_code=200)
async def menu_() -> dict:
    return False #flik(db)

####### ROUTES [USER MANAGEMENT] #######

@app.post("/link", status_code=200)
async def link_(request: LinkRequest):

    # verify token
    token = request.auth_token
    if AUTH_TOKEN_REQUIRED and not verify_token(db, request.user_id, token):
        return {"error": "Invalid token"}

    # check code
    if request.platform_code not in SUPPORTED_PLATFORMS:
        return {"message": "unsupported platform code"}

    # linking user
    try:
        return False #link(db, request.user_id, request.platform_code, request.username, request.password)
    except Exception as e:
        e = str(e).replace('\'','-')
        return {"message": "error", "exception": str(e)}

@app.post("/adduser", status_code=200)
async def adduser(request: SignUpRequest):

    # checking ios token
    token = request.auth_token
    if AUTH_TOKEN_REQUIRED and not verify_ios_token(db, token):
        return {"error": "Invalid token"}

    # generating a new user token
    if AUTH_TOKEN_REQUIRED:
        new_token = str(uuid.uuid4())
        try:
            db.collection(u'USERS').document(request.user_id).set({'token': new_token})
        except Exception as e:
            e = str(e).replace('\'','-')
            return {"message": "user does not exist in firebase", "exception": str(e)}

    # new user template
    USER = {
        'user_id': request.user_id,
        'CREDS' : {},
        'SCHOOLOGY_TASK_IDS' : [],
        'courses' : [],
    }

    # adding user document to firebase
    try:
        db.collection(u'USERS').document(request.user_id).set(USER)
    except Exception as e:
        e = str(e).replace('\'','-')
        return {"message": "error adding user doc to firebase", "exception": str(e)}

    # opening postgres
    ss = Backend_Interface()

    # generating user key
    handler = EM()
    key = handler.serialize_private_key()
    
    # creating the user in postgres
    try:
        response = ss.create_user(request.user_id, key)
        if response is not None:
            return {"message" : "error (assumed)", "exception" : response}
        else:
            return {"message": "no response, assumed success"}
    except Exception as e:
        e = str(e).replace('\'','-')
        return {"message": "error", "exception" : str(e)}

####### ROUTES [GENERAL] #######

@app.get("/ping", status_code=200)
async def ping():
    return {"message": "pong"} 