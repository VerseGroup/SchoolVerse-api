from email import message
from vgem.em import EM

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