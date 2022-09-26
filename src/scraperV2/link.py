# encryption
from vgem import EM

# python imports
import uuid
from datetime import date

# firebase imports
from src.firebaseV2.write import write_creds

def link_schoology(db, e_username, e_password, user_id):
    write_creds(e_username, e_password, user_id, 'sc', db)
