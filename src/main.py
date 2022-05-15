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
from src.requests import ScrapeRequest, LinkRequest

# scraper
from src.webscraper.scraper.run import flik, schoology, veracross

# startup
app = FastAPI()
db = start_firebase()
ss = Backend_Interface()

####### ROUTES [SCRAPER] #######

@app.post("/scrape", status_code=200)
async def scrape_(request: ScrapeRequest):

    if request.platform_code == 'sc':
        return schoology(db, request.username, request.password, request.user_id)
    else:
        return {"message": "unsupported platform code"}


@app.get("/menu", status_code=200)
async def menu():
    return flik(db)

####### ROUTES [USER MANAGEMENT] #######

@app.post("/link", status_code=200)
async def link_(request: LinkRequest):
    return {"message": "link function not yet implemented"}

####### ROUTES [GENERAL] #######

@app.get("/ping", status_code=200)
async def ping():
    return {"message": "pong"} 