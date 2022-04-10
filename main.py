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

# scraping function request body
class ScrapeRequest(BaseModel):
    user_id: int
    platform_code: str
    token: str

@app.post("/scrape", status_code=200)
async def scrape_(request: ScrapeRequest):
    status = scrape(user_id=request.user_id, platform_code=request.platform_code, token=request.token, db=db)
    return status

# ensure function request body
class EnsureRequest(BaseModel):
    user_id: int
    platform_code: str

@app.post("/ensure", status_code=200)
async def ensure_(request: EnsureRequest):
    status = ensure(user_id=request.user_id, platform_code=request.platform_code, db=db)
    return status

#### NON-INDIVIDUAL (GENERAL SCHOOLWIDE) EVENTS ####

# flik menu scraping
class MenuRequest(BaseModel):
    year: int
    month: int
    day: int
    mealtype: str
    
@app.post("/menu", status_code=200)
async def menu(request: MenuRequest):
    try:
        menu = scrape_flik(request.mealtype, request.day, request.month, request.year)
        write_menu(menu, db=db)
        return {"message": "success"}
    except Exception as e:
        return {"message": "failed", "error" : str(e)}

# scrape the general schoolwide events
class EventRequest(BaseModel):
    username: str
    password: str

@app.post("/events", status_code=200)
async def events(request: EventRequest):
    return do_events(request.username, request.password)

class CourseRequest(BaseModel):
    user_id: int
    username: str
    password: str

@app.post("/courses", status_code=200)
async def courses(request: CourseRequest):
    try:
        return schoology_courses(request.username, request.password, request.user_id, db)
    except Exception as e:
        return {"message": "failed", "error" : str(e)}

# basic endpoints #

@app.get("/ping", status_code=200)
async def ping():
    return {"message": "pong"}

@app.get("/", status_code=200)
async def root():
    return "404 not found"

@app.get("/kanye", status_code=200)
async def kanye():
    return {"message": "i'm impressed that you found this"}