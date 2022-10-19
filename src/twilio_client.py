from twilio.rest import Client
from dotenv import load_dotenv
import os

APP_SID= "MG190f52ced38f400b2ee059f72dacdff6"

try:
    load_dotenv()
except:
    pass

TOKEN = str(os.environ['TOKEN'])
SID = str(os.environ['SID'])
NUMBER1 = str(os.environ['NUMBER1'])
DEV_NUMBER = str(os.environ['DEV_NUMBER'])

NUMBERS = [NUMBER1,]

def sendMessage(body, number):
    client = Client(SID, TOKEN)
    client.messages.create(to=number, from_=DEV_NUMBER, body=body, messaging_service_sid=APP_SID)

if __name__ == "__main__":
    for number in NUMBERS:
        sendMessage("TEST", number)