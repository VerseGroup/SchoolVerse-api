# connects to the security server and pulls encryption keys

# python imports
import os
import sys
import requests

# adding dir to sys to allow local importing
currentdir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(currentdir)
parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentdir)

# local imports
from vgem import EM

# function that gets key from security server, decrypts it, and returns credentials
def get_credentials(user_id, platform_code):
    
    # a URL Session to manage requests
    s = requests.Session()