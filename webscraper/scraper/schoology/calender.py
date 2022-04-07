# python imports
from datetime import datetime

# internal imports 
from webscraper.models import Event, Task

# external imports
import markdownify as md 

class Temp_Event:
    def __init__(self, id, name, date):
        self.name = name
        self.date = date
        self.id = id

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'date': self.date
        }

def parse_event(event) -> Temp_Event:
    return Temp_Event(id=event['id'], name=event['title'], date=event['start']).serialize()

def parse_task(task) -> Task:
    platform_information={
        "platform_code" : "sc",
        "assignment_code": task['content_id'],
    }
    description = task['body']
    
    # converting html description to markdown so it can be displayed in the app
    description = md.markdownify(description)

    return Task(name=task['titleText'], due_date=task['start'], course_id=task['realm_id'], course_name=task['content_title'], platform_information=platform_information, description=description).serialize()

def parse_calender(calender_json) -> dict:

    events = []
    tasks = []

    for object in calender_json:

        # check to make sure relevant date
        objectday = int(object['start'].split(" ")[0].split("-")[0])
        todaysday = datetime.now().day
        if todaysday > objectday:
            continue
        
        if object['e_type'] == "event":
            events.append(parse_event(object))
        elif object['e_type'] == "assignment":
            tasks.append(parse_task(object))

    return {
        "events" : events,
        "tasks" : tasks,
    }