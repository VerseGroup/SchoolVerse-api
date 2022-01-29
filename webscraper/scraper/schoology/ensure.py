# python imports
import os
import sys

# adding dir to sys to allow local importing
currentdir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(currentdir)

# local imports
'''
from auth import auth_schoology

def ensure(username, password):
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
'''
