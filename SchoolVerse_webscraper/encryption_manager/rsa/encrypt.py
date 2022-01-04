# python imports
import os
import sys

# adding dir to sys to allow local importing
currentdir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(currentdir)

# crypto imports
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

def encrypt(message, private_key=None, public_key=None):
    
    # checking to see if a key is present, setting the key based on params
    if private_key is None and public_key is None:
        return {
            'message' : 'no key entered'
        }
    
    # encoding message to binary to be encrypted
    message = message.encode('utf-8')

    # encrypting with sha256 based on given key
    if public_key is not None:
        encrypted_message = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
        )
    else: 
        encrypted_message = private_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
        )

    return encrypted_message
