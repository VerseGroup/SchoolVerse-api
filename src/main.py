# python imports
import os

# external imports 
from fastapi import FastAPI
from pydantic import BaseModel
from vgem import EM

# firebase
from src.webscraper.firebase.auth import start_firebase

# startup
app = FastAPI()
db = start_firebase()

# ROUTES [MAIN] #

class ScrapeRequest(BaseModel):
    user_id: int
    platform_code: str
    token: str

@app.post("/scrape", status_code=200)
async def scrape_(request: ScrapeRequest):
    return {"message": "Hello World"}

class LinkRequest(BaseModel):
    user_id: int
    platform_code: str
    token: str
    username: str
    password: str

@app.post("/link", status_code=200)
async def link_(request: LinkRequest):
    return {"message": "link function not yet implemented"}

# ROUTES [GENERAL] #

@app.get("/ping", status_code=200)
async def ping():
    return {"message": "pong"}

@app.get("/kanye", status_code=200)
async def kanye():
    return {"message": "what?"}

from src.webscraper.scraper.flik.scraper import scrape_flik
from src.webscraper.firebase.menu import write_menu
from datetime import date

def flik(today=True):
    if today==True:
        today = date.today()
        today = today.strftime("%d/%m/%Y")
        today = today.split('/')

    menu = scrape_flik(today[0], today[1], today[2])
    write_menu(menu, db)

    return "Finished Flik"

@app.get("/menu", status_code=200)
async def menu():
    return flik()