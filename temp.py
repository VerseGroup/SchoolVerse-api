from vgem import EM
handler = EM()
key = handler.serialize_private_key()
file = open('private_key.pem', 'w')
file.write(key)
file.close()