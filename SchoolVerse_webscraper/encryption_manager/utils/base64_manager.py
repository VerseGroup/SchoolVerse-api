# python imports
import base64

# encode in base64
def encode(message):
    coded_message = base64.b64encode(message)
    coded_message = coded_message.decode('utf-8')
    return coded_message

# decode in base64
def decode(coded_message):
    coded_message = coded_message.encode('utf-8')
    message = base64.b64decode(coded_message)
    message = message.decode('utf-8')
    return message
