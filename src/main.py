# python imports
import os

# external imports 
from fastapi import FastAPI
from pydantic import BaseModel
from vgem import EM

# firebase
from src.webscraper.firebase.auth import start_firebase

# flik
from src.webscraper.scraper.flik.scraper import scrape_flik
from src.webscraper.firebase.menu import write_menu
from datetime import date

# startup
app = FastAPI()
db = start_firebase()

####### ROUTES [MAIN] #######

class ScrapeRequest(BaseModel):
    user_id: int
    platform_code: str
    token: str

@app.post("/scrape", status_code=200)
async def scrape_(request: ScrapeRequest):
    return {"message": "Will finish later"}

class LinkRequest(BaseModel):
    user_id: int
    platform_code: str
    token: str
    username: str
    password: str

@app.post("/link", status_code=200)
async def link_(request: LinkRequest):
    return {"message": "link function not yet implemented"}

####### ROUTES [GENERAL] #######

@app.get("/ping", status_code=200)
async def ping():
    return {"message": "pong"} 

'''
@app.get("/kanye", status_code=200)
async def kanye():
    return {"message": "what?"}
'''

####### MENU #######

def flik(useToday=True, day=None):
    if useToday:
        today = date.today()
        today = today.strftime("%d/%m/%Y")
        day = today.split('/')

    menu = scrape_flik(day[0], day[1], day[2])
    write_menu(menu, db)

    return {"message": "successfully scraped flik"}

@app.get("/menu", status_code=200)
async def menu():
    return flik()
