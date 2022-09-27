""" # python imports

# local imports
from src.webscraper.scraper.schoology.auth import auth_schoology

# making sure that the schoology username and password are correct
def ensure_schoology(username, password):
    s = auth_schoology(username, password)

    response = s.get('https://hackley.schoology.com/home')
    content = response.text

    if '<span class="h3 sign-in-header">Sign in to Schoology</span>' in content:
        return False
    else:
        return True
 """