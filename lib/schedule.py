# imports
import os, sys
from vgem import EM

# append paths
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parent_dir)

# veracross
from src.webscraper.scraper.veracross.run import scrape_veracross

# firebase
from src.webscraper.firebase.credentials import get_encrypted_credentials
from src.webscraper.firebase.schedule import write_schedule
from src.webscraper.firebase.auth import start_firebase

# postgres
from src.postgres.crud import Backend_Interface

# This script cannot run on M1, and is designed to be left running #

def update_schedules(db, ss):

    failed = []
    success = []
    
    # get the list of users that need schedules
    ids = db.collection(u'QUEUES').document(u'schedules_queue').get().to_dict()['user_ids']

    for id in ids:

        try: 
            # get user ciphers
            creds = get_encrypted_credentials(id, 'sc', db)
            cusername = creds['username_ciphertext']
            cpassword = creds['password_ciphertext']

            # get user keys
            key = ss.get_user_keychain(id)

            # decrypt user ciphers
            handler = EM(serialized_private_key=key)
            username = handler.decrypt_rsa(cusername, True)
            password = handler.decrypt_rsa(cpassword, True)

            # scrape veracross and write to firebase
            schedule = scrape_veracross(username, password)
            write_schedule(id, schedule, db)

            # remove user from queue
            ids.remove(id)

            success.append(id)
        
        except Exception as e:
            failure = {
                "id": id,
                "exception": str(e)
            }
            failed.append(failure)

    # write queue back to firebase
    db.collection(u'QUEUES').document(u'schedules_queue').set({'user_ids': ids})

    return {"message" : "finished", "successes": success, "failed": failed}

if __name__ == "__main__":
    try: 
        db = start_firebase()
        ss = Backend_Interface()
    except Exception as e:
        db = None
        ss = None
        print(f"failed with error \"{str(e)}\"")

    try:
        if db is not None and ss is not None:    
            returns = update_schedules(db, ss)
            db.close()
            print(returns)
    except Exception as e:
        print(f"failed with error \"{str(e)}\"")