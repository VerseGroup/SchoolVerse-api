# external imports 
from fastapi import FastAPI
from webscraper.firebase import get_encrypted_credentials, write_creds, write_tasks, write_schedule
from webscraper.scraper.schoology import scrape_schoology
from webscraper.scraper.veracross import scrape_veracross
from vgem import EM

app = FastAPI()

@app.post("/scrape/{user_id}/{platform_code}", status_code=200)
async def scrape(user_id: int, platform_code: str):
    
    # get ciphers from firebase
    try:
        cred_dict = get_encrypted_credentials(user_id, platform_code)
        username = cred_dict['username_ciphertext']
        password = cred_dict['password_ciphertext']
    except:
        return {"message": "Invalid user ID"}

    # get keys from keychain
    try:
        serialized_private_key = "test"
    except:
        return {"message" : "error with reading key from keychain"}

    # decrypt ciphers with keys
    handler = EM(serialized_private_key=serialized_private_key)
    try:
        username = handler.decrypt_rsa(username, True)
        password = handler.decrypt_rsa(password, True)
    except:
        return {"message": "error decrypting ciphers"}

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