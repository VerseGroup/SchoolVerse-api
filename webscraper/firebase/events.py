def write_events(events, db):
    for event in events:
        write_event(event, db)

def write_event(event, db):
    if check_event_exists(event, db) == False:
        doc_name = f"{event['id']}"
        db.collection(u'EVENTS').document(doc_name).set(event)

        existing_events = db.collection(u'EVENTS').document('EXISTING_EVENTS').get().to_dict()['EVENTS']
        db.collection(u'EVENTS').document("EXISTING_EVENTS").update({"EVENTS": existing_events.append(event['id'])})

def check_event_exists(event, db):
    existing_events_dict = db.collection(u'EVENTS').document('EXISTING_EVENTS').get().to_dict()
    existing_events = existing_events_dict['EVENTS']
    for existing_event in existing_events:
        if existing_event == event['id']:
            return True
    return False
