# python imports
import os
import sys

# adding dir to sys to allow local importing
currentdir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(currentdir)

# local imports
from utils.decrypt import decrypt
from utils.encrypt import encrypt
from utils.key_handler import generate_keys, serialize_keys, deserialize_keys, deserialize_private_key, deserialize_public_key

# a class to easily manage rsa encryption
class EncryptionHandler():

    def __init__(self, serialized_private_key = None, serialized_public_key = None):
        
        # starting a new private/public key group
        if serialized_private_key is None and serialized_public_key is None:
            key_dict = generate_keys()
            
            self.private_key = key_dict['private_key']
            self.public_key = key_dict['public_key']

        # constructing object with both keys
        if serialized_public_key is not None and serialized_private_key is not None:
            deserialized_key_dict = deserialize_keys(serialized_private_key, serialized_public_key)
            
            self.private_key = deserialized_key_dict['private_key']
            self.public_key = deserialized_key_dict['public_key']

        # constructing object with just private key
        if serialized_public_key is None and serialized_private_key is not None:
            deserialized_private_key = deserialize_private_key(serialized_private_key)
            
            self.public_key=None
            self.private_key=deserialized_private_key

        # constructing object with just public key
        if serialized_private_key is None and serialized_public_key is not None:
            deserialized_public_key = deserialize_private_key(serialized_public_key)
            
            self.private_key=None
            self.public_key=deserialized_public_key 

    # serializes object's keys for shipping
    def serialize_keys(self):
        return serialize_keys(self.private_key, self.public_key)

    # encrypts a message (str) with either avaiable key
    def encrypt(self, message):
        return encrypt(message, self.private_key, self.public_key)

    # decrypts encrypted message using private key
    def decrypt(self, message):
        if self.private_key is not None:
            try:
                return {
                    "message" : "success",
                    "code" : '0',
                    "decrypted_message" : decrypt(message, self.private_key)
                }
            except:
                return {
                    "message" : "error decrypting",
                    "code" : '1-a',
                }
        else:
            return {
                "message" : "not authorized to decrypt (no private key)",
                "code" : "1c"
            }
