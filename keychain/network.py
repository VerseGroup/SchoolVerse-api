import requests
from keychain.urls import BASE_URL, GET_KEY, ADD_KEY

def get_key(firebase_id, platform_code, token):
    data = {
        'firebase_id': firebase_id,
        'platform_code': platform_code,
        'token': token,
    }
    URL = GET_KEY
    response = requests.get(URL, params=data).json()

    if response is None:
        return None
    else:
        return response['data']

