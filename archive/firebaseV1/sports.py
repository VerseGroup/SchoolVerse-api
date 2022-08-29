# TODO: CLEAN THIS CODE 

from datetime import datetime

def write_sports(events, db):
    for event in events:
        write_sport(event, db)

def write_sport(event, db):
    if check_sports_event_exists(event, db) == False:
        doc_name = f"{event['id']}"

        db.collection(u'SPORTS').document(doc_name).set(event)
        
        existing_events = db.collection(u'SPORTS').document('EXISTING_SPORTS').get().to_dict()['SPORTS']

        if existing_events is None:
            existing_events = [event['platform_information']['id']]
        else:
            existing_events.append(event['platform_information']['id'])
        
        db.collection(u'SPORTS').document("EXISTING_SPORTS").set({"SPORTS": existing_events})
    else:
        print(f"SPORT {event['id']} already exists")

def check_sports_event_exists(event, db):
    existing_events_dict = db.collection(u'SPORTS').document('EXISTING_SPORTS').get().to_dict()
    existing_events = existing_events_dict['SPORTS']
    if existing_events is not None:
        if event['platform_information']['id'] in existing_events:
            return True
    return False
