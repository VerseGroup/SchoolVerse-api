# writes menu to firebase
def write_menu(menu, db):

    for key in menu:
        date = key
        menu_ref = db.collection(u'MENUS').document(date)
        to_write = menu[key]
        del to_write['date']
        menu_ref.set(to_write)
