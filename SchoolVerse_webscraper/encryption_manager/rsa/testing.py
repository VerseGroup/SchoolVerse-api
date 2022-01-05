# python imports
import os
import sys

# adding dir to sys to allow local importing
currentdir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(currentdir)

# local imports for testing
from encryption_handler import EncryptionHandler

handler = EncryptionHandler()
print(handler.private_key)
print(handler.public_key)
print()

serialized_keys = handler.serialize_keys()
print(serialized_keys)
print()

message = "test message"
encrypted_message = handler.encrypt(message)
print(encrypted_message)
print()

decrypted_message = handler.decrypt(encrypted_message)
print(decrypted_message)