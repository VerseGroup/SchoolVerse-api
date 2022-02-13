# python imports
import os
from click import pass_context

# external imports 
from fastapi import FastAPI
from pydantic import BaseModel
from vgem import EM
from webscraper.firebase.auth import start_firebase

# secrets
file = open('secrets/private_key.pem', 'r')
SS_KEY = file.read()
file.close()
handler = EM(serialized_private_key=SS_KEY)

app = FastAPI()
db = start_firebase()

# the main scraping function
from webscraper.scrape import scrape
from webscraper.ensure import ensure

# flik functions
from webscraper.scraper.flik.scraper import scrape_flik
from webscraper.firebase.menu import write_menu

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
        return {"message": str(e)}

# veracross events scraping
class EventRequest(BaseModel):
    year: int
    month: int
    day: int

@app.post("/events", status_code=200)
async def events(request: EventRequest):
    pass

@app.get("/ping", status_code=200)
async def ping():
    return {"message": "pong"}

@app.get("/", status_code=200)
async def root():
    return "404 not found"

@app.get("/kanye", status_code=200)
async def kanye():
    return {"message": "i'm impressed that you found this"}