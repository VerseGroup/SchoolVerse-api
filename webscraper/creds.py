from vgem import EM
from webscraper.firebase import get_encrypted_credentials

def get_creds(user_id, platform_code):
    # get ciphers from firebase
    try:
        cred_dict = get_encrypted_credentials(user_id, platform_code)
        username = cred_dict['username_ciphertext']
        password = cred_dict['password_ciphertext']
    except:
        return {"message": "Invalid user ID"}

    # get keys from keychain
    try:
        pass
    except Exception as e:
        return {"message" : "error with reading key from keychain", "error" : str(e)}

    # decrypt ciphers with keys
    try:
        handler = EM()
        username = handler.decrypt_rsa(username, True)
        password = handler.decrypt_rsa(password, True)
    except Exception as e:
        return {"message": "error decrypting ciphers", "error" : str(e)}
    
    return {
        "username" : username,
        "password" : password
    }