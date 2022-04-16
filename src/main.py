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