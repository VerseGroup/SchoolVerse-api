""" from datetime import datetime

# writes menu to firebase
def write_menu(menu, db):

    menu_reference = db.collection(u'MENUS')
    menu_docs = menu_reference.list_documents()
    for doc in menu_docs:
        menu_reference.document(doc.id).delete()

    for key in menu:
        date = key
        menu_ref = db.collection(u'MENUS').document(date)
        to_write = menu[key]
        to_write['breakfast'] = to_write['breakfast']['food']
        to_write['lunch'] = to_write['lunch']['food']
        to_write['dinner'] = to_write['dinner']['food']
        to_write['date'] = convert_flik_date(date)
        menu_ref.set(to_write)

def convert_flik_date(date):
    date = date.split('-')
    year = date[0]
    month = date[1]
    day = int(date[2]) + 1 # fixing a glitch where the date is off by one 

    return datetime(int(year), int(month), int(day))



 """
