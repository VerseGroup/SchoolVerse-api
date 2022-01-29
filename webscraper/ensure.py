# ensuring that user credentials work

# local imports
from webscraper.scraper.schoology.ensure import ensure
from webscraper.creds import get_creds

def ensure(user_id, platform_code):
    # get creds
    creds = get_creds(user_id, platform_code)
    if 'message' in creds:
        return creds['message']
    else:
        username = creds['username']
        password = creds['password']

    # test creds
    if platform_code == "sc":
        return ensure(username, password)
