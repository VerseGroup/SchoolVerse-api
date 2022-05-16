# python imports
import os

# external imports 
from fastapi import FastAPI
from pydantic import BaseModel
from vgem import EM

# firebase
from src.webscraper.firebase.auth import start_firebase
from src.postgres.crud import Backend_Interface

# requests
from src.requests import ScrapeRequest, LinkRequest, SignUpRequest

# scraper
from src.webscraper.scraper.run import flik, schoology, veracross

# linking
from src.webscraper.scraper.run import link

# startup
app = FastAPI()
db = start_firebase()

####### ROUTES [SCRAPER] #######

@app.post("/scrape", status_code=200)
async def scrape_(request: ScrapeRequest):
    ss = Backend_Interface()
    try:
        if request.platform_code == 'sc':
            return schoology(db, ss, request.user_id)
        else:
            return {"message": "unsupported platform code"}
    except Exception as e:
        return {"message": str(e)}



@app.get("/menu", status_code=200)
async def menu():
    return flik(db)

####### ROUTES [USER MANAGEMENT] #######

@app.post("/link", status_code=200)
async def link_(request: LinkRequest):
    ss = Backend_Interface()
    try:
        return link(db, ss, request.user_id, request.platform_code, request.username, request.password)
    except Exception as e:
        return {"message": str(e)}

@app.post("/adduser", status_code=200)
async def adduser(request: SignUpRequest):
    ss = Backend_Interface()
    handler = EM()
    key = handler.serialize_private_key()
    try:
        response = ss.create_user(request.userid, key)
        if response is not None:
            return response
        else:
            return {"message": "no response, assumed success"}
    except Exception as e:
        return {"message": str(e)}

####### ROUTES [GENERAL] #######

@app.get("/ping", status_code=200)
async def ping():
    return {"message": "pong"} 