# decrypts ciphertext with external key

# python imports
from cryptography.fernet import Fernet

# decrypts ciphertext using external key
def decrypt(ciphertext, key):
    
    # fernet object to hold the key
    f = Fernet(key)
    
    # using the package to decrypt
    data = f.decrypt(ciphertext)
    
    return data