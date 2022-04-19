from datetime import datetime

# writes menu to firebase
def write_menu(menu, db):

    for key in menu:
        date = key
        menu_ref = db.collection(u'MENUS').document(date)
        to_write = menu[key]
        thedate = to_write['breakfast']['date']
        to_write['breakfast'] =to_write['breakfast']['food']
        to_write['lunch'] =to_write['lunch']['food']
        to_write['dinner'] =to_write['dinner']['food']
        to_write['date'] = convert_date(thedate)
        menu_ref.set(to_write)

def convert_date(date):
    date = date.split('-')
    year = date[0]
    month = date[1]
    day = date[2]

    return datetime(int(year), int(month), int(day))




