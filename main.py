# python imports
import os

# external imports 
from fastapi import FastAPI
from pydantic import BaseModel
from vgem import EM

# secrets
file = open('secrets/private_key.pem', 'r')
SS_KEY = file.read()
file.close()
handler = EM(serialized_private_key=SS_KEY)

app = FastAPI()

# the main scraping function
from webscraper.scrape import scrape
from webscraper.ensure import ensure

# flik functions
from webscraper.scraper.flik.scraper import scrape_flik
from webscraper.firebase.write_menu import write_menu

# scraping function request body
class ScrapeRequest(BaseModel):
    user_id: int
    platform_code: str
    token: str

@app.post("/scrape", status_code=200)
async def scrape_(request: ScrapeRequest):
    status = scrape(user_id=request.user_id, platform_code=request.platform_code, token=request.token)
    return status

# ensure function request body
class EnsureRequest(BaseModel):
    user_id: int
    platform_code: str

@app.post("/ensure", status_code=200)
async def ensure_(request: EnsureRequest):
    status = ensure(user_id=request.user_id, platform_code=request.platform_code)
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
        write_menu(menu)
        return {"message": "success"}
    except Exception as e:
        return {"message": str(e)}

@app.get("/ping", status_code=200)
async def ping():
    return {"message": "pong"}

@app.get("/", status_code=200)
async def root():
    return "404 not found"