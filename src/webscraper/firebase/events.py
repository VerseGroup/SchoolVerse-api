from datetime import datetime

def write_events(events, db):
    for event in events:
        write_event(event, db)

def write_event(event, db):
    if check_event_exists(event, db) == False:
        doc_name = f"{event['id']}"
        
        try:
            start = convert_date(event['start_date'], event['start_time'])
            end = convert_date(event['end_date'], event['end_time'])
        except:
            start = "something broke"
            end = "something broke"

        event.pop('start_date')
        event.pop('start_time')
        event.pop('end_date')
        event.pop('end_time')
        
        event['start'] = start
        event['end'] = end

        if "Day" in event['description']:
            event.pop('location')
            event.pop('end')
            event.pop('description')
            event['day'] = event['name']
            event.pop('name')
            event['date'] = event['start']
            event.pop('start')

            db.collection(u'DAYS').document(doc_name).set(event)

        else:
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
        if event['platform_information']['event_id'] in existing_events:
            return True
    return False

def convert_date(date, time):

    if date is None:
        return None
    
    date = date.split("/")
    
    month = date[0]
    day = date[1]
    year = date[2]

    if time is None:
        return datetime(int(year), int(month), int(day))

    times = time.split(" ")
    
    time = times[0].split(":")
    hour = time[0]
    minute = time[1]

    am_pm = times[1]
    if am_pm == "PM":
        hour = int(hour) + 12

    date_object = datetime(int(year), int(month), int(day), int(hour), int(minute))
    
    return date_object

