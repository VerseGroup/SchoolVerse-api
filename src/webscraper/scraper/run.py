# encryption
from vgem import EM

# flik
from src.webscraper.scraper.flik.scraper import scrape_flik
from src.webscraper.firebase.menu import write_menu
from datetime import date

# schoology
from src.webscraper.firebase.tasks import write_tasks
from src.webscraper.scraper.schoology.scraper import scrape_schoology
from src.webscraper.firebase.courses import write_courses
from src.webscraper.scraper.schoology.ensure import ensure_schoology
from src.webscraper.firebase.credentials import get_encrypted_credentials, write_creds

# veracross
from src.webscraper.scraper.veracross.run import scrape_veracross
from src.webscraper.firebase.schedule import write_schedule
from src.webscraper.firebase.events import write_events
from src.webscraper.scraper.veracross.events import get_events

# postgres
from src.postgres.crud import Backend_Interface

def schoology(db, ss, user_id):

    # getting keys
    try:
        key = ss.get_user_keychain(user_id)
    except Exception as e:
        return {"message": "user does not exist postgres", "exception": str(e)}
    
    handler = EM(serialized_private_key=key)

    # getting ciphers
    try:
        creds = get_encrypted_credentials(user_id, 'sc', db)
    except Exception as e:
        return {"message": "user does not exist in firebase", "exception": str(e)}
    c_username = creds['username_ciphertext']
    c_password = creds['password_ciphertext']

    # getting username
    username = handler.decrypt_rsa(c_username, True)
    password = handler.decrypt_rsa(c_password, True)

    returns = scrape_schoology(username, password)
    tasks = returns['tasks']
    write_tasks(tasks, user_id, db)

    return {"message": "success"}

def flik(db, useToday=True, day=None):
    if useToday:
        today = date.today()
        today = today.strftime("%d/%m/%Y")
        day = today.split('/')

    menu = scrape_flik(day[0], day[1], day[2])
    write_menu(menu, db)

    return {"message": "success"}

def veracross(db, username, password):
    days = scrape_veracross(username, password)
    write_schedule(1, days, db)

    return {"message": "success"}

def events(db, username, password):
    events = get_events(username, password)
    write_events(events, db)

    return {"message": "success"}

def create_user(ss, user_id):
    handler = EM()
    key = str(handler.serialize_private_key())
    ss.create_user(user_id, key)

def link(db, user_id, platform_code, username, password):

    ss = Backend_Interface()

    try:
        key = ss.get_user_keychain(user_id)
    except:
        return {"message": "user does not exist in postgres"}
   
    if key is None:
        response = create_user(ss, user_id)
        if response is not None:
            return {"message": "user creation failed", "exception" : str(response)}

    if platform_code == 'sc':
        if not ensure_schoology(username, password):
            return {"message": "schoology credentials are incorrect"}
        else:
            handler = EM(serialized_private_key=key)
            username_cipher = handler.encrypt_rsa(username, True)
            password_cipher = handler.encrypt_rsa(password, True)
            try:
                write_creds(username_cipher, password_cipher, user_id, platform_code, db)
            except:
                return {"message": "user does not exist in firebase"}

    elif platform_code == 'vc':
        handler = EM(serialized_private_key=key)
        username_cipher = handler.encrypt_rsa(username, True)
        password_cipher = handler.encrypt_rsa(password, True)
        try:
            write_creds(username_cipher, password_cipher, user_id, platform_code, db)
        except:
            return {"message": "user does not exist in firebase"}

        try:
            objectives = db.collection(u'SCRAPER_OBJECTIVES').document(f'newusers')
            doc = objectives.get()
    
            if doc.exists:
                doc_dict = doc.to_dict()
            else:
                return {"message": "firebase scraper objectives document does not exist"}

            for user in doc_dict['newusers']:
                if user == user_id:
                    return {"message": "user already exists in firebase scraper objectives"}

            doc_dict = doc_dict['newusers'].append(user_id)
            objectives.set(doc_dict)
            
        except:
            return {"message": "firebase scraper objectives document error"}
    
    return {"message": "success"}
