def write_events(events, db):
    for event in events:
        write_event(event, db)

def write_event(event, db):
    if check_event_exists(event, db) == False:
        doc_name = f"{event['id']}"
        db.collection(u'EVENTS').document(doc_name).set(event)

        existing_events = db.collection(u'EVENTS').document('EXISTING_EVENTS').get().to_dict()['EVENTS']

        if existing_events is None:
            existing_events = [event['platform_information']['event_id']]
        else:
            existing_events.append(event['platform_information']['event_id'])
        db.collection(u'EVENTS').document("EXISTING_EVENTS").set({"EVENTS": existing_events})
    else:
        print(f"Event {event['id']} already exists")

def check_event_exists(event, db):
    existing_events_dict = db.collection(u'EVENTS').document('EXISTING_EVENTS').get().to_dict()
    existing_events = existing_events_dict['EVENTS']
    if existing_events is not None:
        if event['id'] in existing_events:
            return True
    return False
