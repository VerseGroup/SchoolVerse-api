# local imports
from main import db

# writes inputted credential information to firebase (add a platform code parameter in the future)
def write_creds(username, password, user_id, platform_code):
    data = {f"{platform_code}" : [username, password]}
    formatted_data = {"CREDS" : data}
    user_ref = db.collection(u'USERS').document(f'{user_id}').update(formatted_data)