# crypto imports
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# generates a new connected private and public key (as objects)
def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    return {
        'private_key' : private_key,
        'public_key' : public_key
    }

# serializes key objects into plaintext
def serialize_keys(private_key=None, public_key=None):

    returns = {}

    if private_key is not None:
        serialized_private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
        )
        returns['serialized_private_key'] = serialized_private_key

    if public_key is not None:
        serialized_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        returns['serialized_public_key'] = serialized_public_key

    return returns

# converts plaintext public key into key object
def deserialize_public_key(serialized_public_key):
    public_key = serialization.load_pem_public_key(
        serialized_public_key,
        backend=default_backend()
    )
    return public_key

# converts plaintext private key into key object
def deserialize_private_key(serialized_private_key):
    private_key = serialization.load_pem_private_key(
        serialized_private_key,
        password=None,
        backend=default_backend()
    )

    return private_key

# converts both keys from plaintext to key objects as once (if necessary)
def deserialize_keys(serialized_private_key, serialized_public_key):
    
    public_key = deserialize_public_key(serialized_public_key)
    private_key = deserialize_private_key(serialized_private_key)

    return {
        'private_key' : private_key,
        'public_key' : public_key
    }