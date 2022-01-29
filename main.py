# external imports 
from fastapi import FastAPI

app = FastAPI()

# the main scraping function
from webscraper.scrape import scrape
from webscraper.ensure import ensure

@app.post("/scrape/{user_id}/{platform_code}", status_code=200)
async def scrape_(user_id: int, platform_code: str):
    return scrape(user_id=user_id, platform_code=platform_code)
    
@app.get("/ensure/{user_id}/{platform_code}", status_code=200)
async def ensure_(user_id: int, platform_code: str):
    return ensure(user_id=user_id, platform_code=platform_code)
