# writes menu to firebase
def write_menu(menu, type, db):
    menu = {"menu": menu}

    menu_ref = db.collection(u'MENUS').document(type)
    menu_ref.set(menu)
