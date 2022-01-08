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

# external imports
from dotenv import load_dotenv

# gathering secrets
load_dotenv()
URL = os.getenv('SS_URL')

# local imports
from encryption_manager import EncryptionHandler

# function that gets key from security server, decrypts it, and returns credentials
def get_credentials(user_id, platform_code):
    
    # a URL Session to manage requests
    s = requests.Session()