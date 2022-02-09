# imports
from main import db

# writes menu to firebase
def write_menu(menu):
    menu = {"menu": menu}

    menu_ref = db.collection(u'GENERAL').document('menu')
    menu_ref.set(menu)
