# decrypts ciphertext with external key

# python imports
from cryptography.fernet import Fernet

# decrypts ciphertext using external key
def decrypt(ciphertext, key):
    
    # fernet only works with bytes
    key = key.encode('utf-8')
    ciphertext = ciphertext.encode('utf-8')

    # fernet object to hold the key
    f = Fernet(key)
    
    # using the package to decrypt
    data = f.decrypt(ciphertext)
    
    return data.decode('utf-8') # need to decode to get a string