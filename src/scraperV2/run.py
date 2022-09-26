# encryption
from vgem import EM

# config
from src.config import AUTH_TOKEN_REQUIRED

# token
import uuid

# dates
from datetime import date

# flik
from src.scraperV2.fk import scrape_flik
from src.firebaseV2.write import write_menu

# schoology
from src.firebaseV2.write import write_tasks, write_courses, write_creds
from src.scraperV2.sc import scrape_schoology, ensure_schoology
from src.firebaseV2.read import get_encrypted_credentials

# veracross
from src.firebaseV2.write import write_schedule, write_events
from scraperV2.vc.vc import scrape_veracross, get_events

def schoology(db, ss, user_id):

    # getting keys
    try:
        key = ss.get_user_keychain(user_id)
    except Exception as e:
        e = str(e).replace('\'','-')
        return {"message": "user does not exist in postgres", "exception": str(e)}
    
    handler = EM(serialized_private_key=key)

    # getting ciphers
    try:
        creds = get_encrypted_credentials(user_id, 'sc', db)
    except Exception as e:
        e = str(e).replace('\'','-')
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

# this is a helper function for the link function below
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
            objectives = db.collection(u'QUEUES').document(f'schedule_queue')
            doc = objectives.get()
    
            if doc.exists:
                doc_dict = doc.to_dict()
            else:
                return {"message": "firebase scraper objectives document does not exist"}

            newusers = doc_dict['user_ids']

            for user in newusers:
                if user == user_id:
                    return {"message": "user already exists in firebase scraper objectives"}

            newusers.append(user_id)
            objectives.update({'user_ids': newusers})
            
        except Exception as e:
            e = str(e).replace('\'','-')
            return {"message": "firebase scraper objectives document error", "exception": str(e)}
    
    return {"message": "success"}
