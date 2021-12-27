# python imports
import os
import sys

# external imports
from bs4 import BeautifulSoup

# adding directories for local imports
parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentdir)
currentdir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(currentdir)

# internal imports
from ...models import Task
from utils import parse_link_to_course_code

# making references so variables save over iterations
current_date = None

# parsing html file into array of task objects
def parse_html(html_file):
    soup = BeautifulSoup(html_file, 'html.parser')

    upcoming_list = soup.find("div", class_="upcoming-list")
    children = upcoming_list.contents

    tasks = []
    
    for child in children:
        # sifting the soup
        tag = child.name
        if tag is None or tag != "div":
            continue
        
        # pulling classes to identify tags
        classes = child['class']

        # populating dates
        if "date-header" in classes:
            current_date = str(child.contents[0].string).strip()
        
        # populating assignments
        if "course-event" in classes:
            h4_children = child.contents[0].contents

            assignment_name = h4_children[1].string

            assignment_code = parse_link_to_course_code(h4_children[1].attrs['href'])
            platform_information = {
                "code" : "sc",
                "assignment_code" : assignment_code
            }
            
            # use uuid or something instead
            task = Task(id=1, name=assignment_name, due_date= current_date, platform_information=platform_information)
            tasks.append(task.serialize())

    return tasks
