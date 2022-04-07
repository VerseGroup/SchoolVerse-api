def write_events(events, db):
    for event in events:
        write_event(event, db)

def write_event(event, db):
    if check_event_exists(event, db) == False:
        db.collection(u'EVENTS').set(event)

def check_event_exists(event, db):
    current_data = db.collection(u'EVENTS').get().to_dict()
    for key in current_data:
        if current_data[key]['platform_information']['vc_id'] == event['platform_information']['vc_id']:
            return True
    return False
