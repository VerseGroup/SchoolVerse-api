# imports
from webscraper.firebase.schedule import write_schedule
from webscraper.firebase.tasks import write_tasks
from webscraper.scraper.schoology.scraper import scrape_schoology
from webscraper.scraper.veracross.run import scrape_veracross
from webscraper.creds import get_creds
from keychain.network import get_key
from vgem import EM

def scrape(user_id: int, platform_code: str, token: str, db) -> dict:

    # get credentials
    creds = get_creds(user_id, platform_code, token, db)
    if 'message' in creds:
        return creds['message']
    else:
        username = creds['username']
        password = creds['password']

    # dealing with different platforms
    if platform_code == "sc":
        schoology(username, password, user_id, db)  
    elif platform_code == "vc":
        veracross(username, password, user_id, db)
    else:
        return {"message": "invalid platform code"}
       
    return {"message" : "success"}

def schoology(username, password, user_id, db):
    try:
        tasks = scrape_schoology(username, password)['tasks']
    except:
        return {"message": "Error scraping schoology"}

    try:
        # write tasks to firebase
        write_tasks(tasks, user_id, db)
    except:
        return {"message": "error writing tasks to firebase"}

def veracross(username, password, user_id, db):
    try:
        scraped_content = scrape_veracross(username, password)
        day = scraped_content[0]
        schedule = scraped_content[1]
    except:
        return {"message": "Error scraping veracross"}

    try:
        # write the schedule to firebase
        write_schedule(user_id, schedule, day, db)
    except:
        return {"message": "error writing schedule to firebase"}