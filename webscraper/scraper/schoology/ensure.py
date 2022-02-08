# python imports

# local imports
from webscraper.scraper.schoology.auth import auth_schoology

# making sure that the schoology username and password are correct
def ensure_schoology(username, password):
    s = auth_schoology(username, password)

    response = s.get('https://hackley.schoology.com/home')
    content = response.text

    if '<span class="h3 sign-in-header">Sign in to Schoology</span>' in content:
        return {
            "message" : "Invalid username or password",
            "code" : "1"
        }
    else:
        return {
            "message" : "Success",
            "code" : "0"
        }

