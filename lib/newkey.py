from vgem import EM
import pyperclip as pc
import os

if __name__ == "__main__":

    user = os.popen('whoami').read()[:-1]

    handler = EM()
    key = handler.serialize_private_key()
    file = open(f'/Users/{user}/Documents/SchoolVerse-webscraper/secrets/test_key.pem', 'w')
    file.write(key)
    file.close()

    public_key = handler.serialize_public_key()
    pc.copy(public_key)