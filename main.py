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

# scraping function request body
class ScrapeRequest(BaseModel):
    user_id: int
    platform_code: str

@app.post("/scrape", status_code=200)
async def scrape_(request: ScrapeRequest):
    status = scrape(user_id=request.user_id, platform_code=request.platform_code) 
    return status

# ensure function request body
class EnsureRequest(BaseModel):
    user_id: int
    platform_code: str

@app.post("/ensure", status_code=200)
async def ensure_(request: EnsureRequest):
    status = ensure(user_id=request.user_id, platform_code=request.platform_code)
    return status

@app.get("/ping", status_code=200)
async def ping():
    return {"message": "pong"}

