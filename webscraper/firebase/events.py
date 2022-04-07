def write_events(events, db):
    for event in events:
        write_event(event, db)

def write_event(event, db):
    db.collection(u'EVENTS').set(event)
