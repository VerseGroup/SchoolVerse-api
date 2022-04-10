# ensuring that user credentials work

# local imports
from webscraper.scraper.schoology.ensure import ensure_schoology
from webscraper.scraper.veracross.ensure import ensure_veracross
from webscraper.creds import get_creds

def ensure(user_id, platform_code, token, db):
    
    # get creds
    creds = get_creds(user_id, platform_code, token, db)
    if 'message' in creds:
        return creds['message']
    else:
        username = creds['username']
        password = creds['password']

    # test creds
    if platform_code == "sc":
        return ensure_schoology(username, password)

    elif platform_code == "vc":
        return ensure_veracross(username, password)
