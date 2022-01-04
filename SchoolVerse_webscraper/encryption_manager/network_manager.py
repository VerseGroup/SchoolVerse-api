# connects to the security server and pulls encryption keys

# python imports
import os
import sys

# adding dir to sys to allow local importing
currentdir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(currentdir)

# external imports
from dotenv import load_dotenv

# gathering secrets
load_dotenv()

# local imports
from .fernet.decrypt import decrypt
from .auth import generate_oauth2_header

# function that gets key from security server, decrypts it, and returns credentials
def get_credentials(user_id, platform_code):
    pass