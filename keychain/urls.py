# getting base url
file = open('secrets/keychain.txt', 'r')
BASE_URL = file.read()
file.close()

GET_KEY = BASE_URL + '/users/getkey'

