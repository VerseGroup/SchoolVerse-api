# python imports
import os
import sys

# adding dir to sys to allow local importing
currentdir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(currentdir)

# local imports
from decrypt import decrypt
from encrypt import encrypt
from key_handler import generate_keys, serialize_keys, deserialize_keys

class EncryptionHandler():

    def __init__(self):
        # generating a new set of keys
        key_dict = generate_keys()
        
        self.private_key = key_dict['private_key']
        self.public_key = key_dict['public_key']

