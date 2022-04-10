# DEPLOYMENT VERSION

# external
from fastapi import FastAPI
from pydantic import BaseModel

# firebase
from webscraper.firebase.auth import start_firebase

# relevant functions
from webscraper.scrape import scrape
from webscraper.ensure import ensure

# config
from config import SUPPORTED_PLATFORMS

def check_platform(platform_code):
    if platform_code not in SUPPORTED_PLATFORMS:
        return False
    else:
        return True

app = FastAPI()
db = start_firebase()

### SCRAPE

class ScrapeRequest(BaseModel):
    user_id: int
    platform_code: str
    token: str

@app.post("/scrape", status_code=200)
async def scrape_(request: ScrapeRequest):

    if not check_platform(request.platform_code):
        return {"message": "invalid platform code"}

    return scrape(user_id=request.user_id, platform_code=request.platform_code,mtoken=request.token, db=db)
    
### ENSURE

class EnsureRequest(BaseModel):
    user_id: int
    platform_code: str
    token: str

@app.post("/ensure", status_code=200)
async def ensure_(request: EnsureRequest):

    if not check_platform(request.platform_code):
        return {"message": "invalid platform code"}

    return ensure(user_id=request.user_id, platform_code=request.platform_code,mtoken=request.token, db=db)