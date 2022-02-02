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
    user_encryption_key: str

@app.post("/scrape", status_code=200)
async def scrape_(request: ScrapeRequest):
    try: 
        user_encryption_key = handler.decrypt_rsa(request.user_encryption_key, True)
    except:
        return {"message": "encryption key did not come from the security server (unauthorized usage of the webscraper)"}

    status = scrape(user_id=request.user_id, platform_code=request.platform_code, encryption_key=user_encryption_key) 

    return status

# ensure function request body
class EnsureRequest(BaseModel):
    user_id: int
    platform_code: str
    user_encryption_key: str

@app.get("/ensure", status_code=200)
async def ensure_(user_id: int, platform_code: str, user_encryption_key: str):
    try:
        user_encryption_key = handler.decrypt_rsa(user_encryption_key, True)
    except:
        return {"message": "encryption key did not come from the security server (unauthorized usage of the webscraper)"}

    status = ensure(user_id=user_id, platform_code=platform_code, encryption_key=user_encryption_key)

    return status

@app.get("/ping", status_code=200)
async def ping():
    return {"message": "pong"}

