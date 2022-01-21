# test the custom encryption manager

from vgem import EM

def test_vgem_encryption_():
    handler = EM()
    message = "a very secret message"

    emessage = handler.encrypt_rsa(message, True)
    dmessage = handler.decrypt_rsa(emessage, True)

    assert message == dmessage

def test_vgem_serialization():
    handler = EM()
    message = "SECRET MESSAGE"

    emessage = handler.encrypt_rsa(message, True)

    key = handler.serialize_private_key()
    handler2 = EM(serialized_private_key=key)
    dmessage = handler2.decrypt_rsa(emessage, True)

    assert message == dmessage

'''
(commented because github auto-pytest on commit doesn't have access to firebase secrets auth)
def test_encrypt_write_to_firebase():
    from webscraper.firebase_manager.write_credentials import write_creds
    from webscraper.firebase_manager.read_encryptions import get_encrypted_credentials

    handler = EM()

    username = "testing"
    password = "testing"

    eusername = handler.encrypt_rsa(username, True)
    epassword = handler.encrypt_rsa(password, True)

    write_creds(eusername, epassword, 1, 'sc')

    creds = get_encrypted_credentials(1, 'sc')

    pusername = creds['username_ciphertext']
    ppassword = creds['password_ciphertext']

    dusername = handler.decrypt_rsa(pusername, True)
    dpassword = handler.decrypt_rsa(ppassword, True)

    assert username == dusername and password == dpassword
'''