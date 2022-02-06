# python imports
import os
import sys
import uuid

# adding dir to sys to allow local importing
currentdir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(currentdir)

# firebase imports
import firebase_admin

# local imports
from auth import db

# writes menu to firebase
def write_menu(menu):
    menu_ref = db.collection(u'GENERAL').document('menu')
    menu_ref.set(menu)
