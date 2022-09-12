from icalendar import Calendar, Event
import requests

def convert_ical_to_json(ical_link):
    r = requests.get(ical_link)
    cal = Calendar.from_ical(r.text)

    # print the calender
    print(cal)

if __name__ == "__main__":
    TEST_LINK = "http://api.veracross.com/hackley/subscribe/EC34541C-40AC-408F-AD72-FF36D99A220C.ics?uid=D517397E-D0B8-4DFA-90DD-7B07A141FA24"
    print(convert_ical_to_json(TEST_LINK))