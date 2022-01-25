# python imports
import os
import sys
from datetime import datetime

# adding parentdirs for internal imports
# adding directories for local imports
parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentdir)
doubleparentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir))
sys.path.append(doubleparentdir)

# internal imports
from models import Event, Task

def parse_event(event):
    pass

def parse_task(task):
    pass

def parse_calender(calender_json):

    events = []
    tasks = []


    for object in calender_json:

        # check to make sure relevant date
        objectday = object['start'].split(" ")[0].split("-")[0]
        todaysday = datetime.now().day
        if todaysday > objectday:
            continue
        
        if object['e_type'] == "event":
            events.append(parse_event(object))
        elif object['e_type'] == "assignment":
            tasks.append(parse_task(object))