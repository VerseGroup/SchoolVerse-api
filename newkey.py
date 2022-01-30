from vgem import EM
import pyperclip as pc

if __name__ == "__main__":
    handler = EM()
    key = handler.serialize_private_key()
    file = open('secrets/private_key.pem', 'w')
    file.write(key)
    file.close()

    public_key = handler.serialize_public_key()
    pc.copy(public_key)