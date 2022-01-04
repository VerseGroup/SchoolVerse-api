import cryptography
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

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

def serialize_keys(private_key, public_key):

    serialized_private_key = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
    )

    serialized_public_key = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return {
        'serialized_private_key' : serialized_private_key,
        'serialized_public_key' : serialized_public_key
    }

def deserialize_public_key(serialized_public_key):
    public_key = serialization.load_pem_public_key(
        serialized_public_key,
        backend=default_backend()
    )
    return public_key

def deserialize_private_key(serialized_private_key):
    private_key = serialization.load_pem_private_key(
        serialized_private_key,
        password=None,
        backend=default_backend()
    )

    return private_key

def deserialize_keys(serialized_private_key, serialized_public_key):
    
    public_key = deserialize_public_key(serialized_public_key)
    private_key = deserialize_private_key(serialized_private_key)

    return {
        'private_key' : private_key,
        'public_key' : public_key
    }

def testing():
    dict = generate_keys()
    dict2 = serialize_keys(private_key=dict['private_key'], public_key=dict['public_key'])
    dict3 = deserialize_keys(serialized_private_key=dict2['serialized_private_key'], serialized_public_key=dict2['serialized_public_key'])
    print(dict3)

#testing()