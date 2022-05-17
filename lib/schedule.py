# imports
from vgem import EM

# databases
from src.webscraper.firebase.auth import start_firebase
from src.webscraper.firebase.credentials import get_encrypted_credentials
from src.webscraper.firebase.schedule import write_schedule
from src.postgres.crud import Backend_Interface

# veracross
from src.webscraper.scraper.veracross import scrape_veracross

def scrape_schedule(user_id):
    ss = Backend_Interface()
    db = start_firebase()

    try:
        key = ss.get_user_keychain(user_id)
    except:
        return {"message": "user not in postgres"}

    try:
        handler = EM(serialized_private_key=key)
    except:
        return {"message": "key not valid"}

    try:
        creds = get_encrypted_credentials(db, user_id)
        username = creds['username_ciphertext']
        password = creds['password_ciphertext']
    except:
        return {"message": "user not in firebase"}

    try: 
        username = handler.decrypt_rsa(username, True)
        password = handler.decrypt_rsa(password, True)
    except:
        return {"message": "credentials not valid"}

    try:
        schedule = scrape_veracross(username, password)
        write_schedule(schedule, user_id, db)
    except:
        return {"message": "schedule not scraped, error with scraper"}

    return {"message": "success"}

if __name__ == "__main__":
    id = input('ID: ')
    print(scrape_schedule(id))

