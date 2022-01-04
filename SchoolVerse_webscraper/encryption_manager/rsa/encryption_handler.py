# python imports
import os
import sys

# adding dir to sys to allow local importing
currentdir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(currentdir)

# local imports
from decrypt import decrypt
from encrypt import encrypt
from key_handler import generate_keys, serialize_keys, deserialize_keys, deserialize_private_key, deserialize_public_key

class EncryptionHandler():

    def __init__(self):
        # generating a new set of keys
        key_dict = generate_keys()
        
        self.private_key = key_dict['private_key']
        self.public_key = key_dict['public_key']

    def __init__(self, serialized_private_key, serialized_public_key):
        deserialized_key_dict = deserialize_keys(serialized_private_key, serialized_public_key)
        
        self.private_key = deserialized_key_dict['private_key']
        self.public_key = deserialized_key_dict['public_key']

    def __init__(self, serialized_private_key):
        deserialized_private_key = deserialize_private_key(serialized_private_key)

        self.public_key=None
        self.private_key=deserialized_private_key

    def __init__(self, serialized_public_key):
        deserialized_public_key = deserialize_private_key(serialized_public_key)

        self.private_key=None
        self.public_key=deserialized_public_key

    def serialize_keys(self):
        return serialize_keys(self.private_key, self.public_key)
