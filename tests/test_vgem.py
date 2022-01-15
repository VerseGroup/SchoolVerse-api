from vgem.em import EM

def test_vgem_encryption_():
    handler = EM()
    message = "a very secret message"

    emessage = handler.encrypt_rsa(message, True)
    dmessage = handler.decrypt_rsa(emessage, True)

    assert message == dmessage