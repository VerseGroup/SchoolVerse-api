# imports
from webscraper.firebase import write_tasks, write_schedule
from webscraper.scraper.schoology.scraper import scrape_schoology
from webscraper.scraper.veracross.run import scrape_veracross
from webscraper.creds import get_creds
from vgem import EM

def scrape(user_id: int, platform_code: str, encryption_key: str):

    # get credentials
    creds = get_creds(user_id, platform_code)
    if 'message' in creds:
        return creds['message']
    else:
        username = creds['username']
        password = creds['password']

    # decrypt credentials with key
    try:
        handler = EM(serialized_private_key=encryption_key)
        username = handler.decrypt_rsa(username, True)
        password = handler.decrypt_rsa(password, True)
    except:
        return {"message": "Invalid encryption key"}


    if platform_code == "sc":
        try:
            # scrape 
            tasks = scrape_schoology(username, password)['tasks']

            # write tasks to firebase
            write_tasks(tasks, user_id)
        except:
            return {"message": "error scraping schoology"}
    
    elif platform_code == "vc":
        try:
            # scrape
            scraped_content = scrape_veracross(username, password)
            day = scraped_content[0]
            schedule = scraped_content[1]

            # write schedule to firebase
            write_schedule(user_id, schedule, day)
        except:
            return {"message": "error scraping veracross"}

    return {"message" : "success"}