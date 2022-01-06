# python imports
import os
import sys

# adding dir to sys to allow local importing
currentdir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(currentdir)

# local imports for testing
from encryption_handler import EncryptionHandler

# case both keys
handler = EncryptionHandler()

message = "test message"
encrypted_message = handler.encrypt(message)

private_key  = handler.serialize_private_key()
handler2 = EncryptionHandler(serialized_private_key=private_key)


decrypted_message = handler2.decrypt(encrypted_message)
print(decrypted_message)

