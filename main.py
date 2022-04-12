# python imports
import os

# external imports 
from fastapi import FastAPI
from pydantic import BaseModel
from vgem import EM

# firebase
from webscraper.firebase.auth import start_firebase

# functions to be used
from webscraper.scrape import scrape, schoology_courses
from webscraper.ensure import ensure
from webscraper.events import do_events
from webscraper.scraper.flik.scraper import scrape_flik
from webscraper.firebase.menu import write_menu

# startup
app = FastAPI()
db = start_firebase()

class ScrapeRequest(BaseModel):
    user_id: int
    platform_code: str
    token: str

@app.post("/scrape", status_code=200)
async def scrape_(request: ScrapeRequest):
    status = scrape(user_id=request.user_id, platform_code=request.platform_code, token=request.token, db=db)
    return status

# ADD A LINK FUNCTION
# LINK - > ENSURE + SCHEDULE + COURSES - > Store/Encrypt everything 

class LinkRequest(BaseModel):
    user_id: int
    platform_code: str
    token: str
    username: str
    password: str

@app.post("/link", status_code=200)
async def link_(request: LinkRequest):
    return {"message": "link function not yet implemented"}

# GENERAL #

@app.get("/ping", status_code=200)
async def ping():
    return {"message": "pong"}

@app.get("/kanye", status_code=200)
async def kanye():
    return {"message": "what?"}