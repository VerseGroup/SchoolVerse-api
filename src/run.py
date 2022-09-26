# encryption
from vgem import EM

# config
from src.config import AUTH_TOKEN_REQUIRED

# token
import uuid
from datetime import date

# scraper imports
from src.scraperV2.sc import scrape_schoology, ensure_schoology
from src.scraperV2.vc.vc import scrape_veracross
from src.scraperV2.vc.auth import get_events
from src.scraperV2.fk import scrape_flik

# firebase
from src.firebaseV2.read import get_encrypted_credentials
from src.firebaseV2.write import write_tasks, write_menu, write_schedule, write_events, write_creds

def create_user(db, user_id):
    key = EM().generate_key()
    pass





def flik(db, useToday=True, day=None):
    if useToday:
        today = date.today()
        today = today.strftime("%d/%m/%Y")
        day = today.split('/')

    menu = scrape_flik(day[0], day[1], day[2])
    write_menu(menu, db)

    return {"message": "success"}