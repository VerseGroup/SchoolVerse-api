from icalendar import Calendar, Event
import requests

def convert_ical_to_json(ical_link):
    r = requests.get(ical_link)
    cal = Calendar.from_ical(r.text)

    events = []
    for component in cal.walk():

        if component.name == "VEVENT":
            event = {}
            event["summary"] = str(component.get("summary"))
            event["id"] = str(component.get("UID"))
            try:
                event["start"] = component.get("dtstart").dt
            except:
                event["start"] = ''
            try:
                event["end"] = component.get("dtend").dt
            except:
                event["end"] = ''
            try:
                event["location"] = str(component.get("location"))
                event["description"] = str(component.get("description"))
            except:
                pass

            if event["location"] == None:
                event["location"] = ''
            if event["description"] == None:
                event["description"] = ''
            
            events.append(event)

    return events

def convert_all_school_events(ical_link):

    r = requests.get(ical_link)
    cal = Calendar.from_ical(r.text)

    events = []
    for component in cal.walk():
         if component.name == "VEVENT":

            event = {}
            event["summary"] = str(component.get("summary"))
            event[""] = str(component.get("UID"))
            event['day'] = component.get("DTSTAMP").dt

            try:
                event['start'] = component.get("DTSTART").dt
                event['end'] = component.get("DTEND").dt
            except:
                event['start'] = ''
                event['end'] = ''

            event['location'] = str(component.get("location"))
            event['description'] = str(component.get("description"))

            
            events.append(event)

    return events

# testing
if __name__ == "__main__":
    TEST_LINK = "http://api.veracross.com/hackley/teams/96556.ics?t=63e028d79709f12c1265f51819ef149a&uid=9172DAAC-C59D-4A00-A48D-DC95D60242DA"
    events = convert_ical_to_json(TEST_LINK)
    #for event in events:
        #print(event, "\n")

    TEST_LINK_2 = "http://api.veracross.com/hackley/subscribe/EC34541C-40AC-408F-AD72-FF36D99A220C.ics?uid=A17227D1-8674-45F8-94E7-2AA4A7323593"
    events2 = convert_all_school_events(TEST_LINK_2)
    for event in events2:
        print(event, "\n")