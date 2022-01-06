# This file contains the code used by schoology.py to parse the schoology website event list 
# Into SchoolVerse task objects

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
from SchoolVerse_webscraper.models import Task
from schoology.utils import parse_link_to_course_code

# making references so variables save over iterations
current_date = None

# parsing html file into array of task objects
def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')

    # isolating the upcoming section of schoology
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

            # using bs4 children proporties to locate/scrape the assignment name
            h4_children = child.contents[0].contents
            for child in h4_children:
                print (child.name)
            print()
            assignment_name = h4_children[1].string

            # parsing an href to an assignment code and then formatting it into a SchoolVerse platform_information dict
            assignment_code = parse_link_to_course_code(h4_children[1].attrs['href'])
            platform_information = {
                "code" : "sc",
                "assignment_code" : assignment_code
            }
            
            # use uuid or something instead
            # creating a task object with the scraped/formatted information
            task = Task(id=1, name=assignment_name, due_date=current_date, platform_information=platform_information)
            
            # probably change to return task objects instead of serialized, then can append an array of tasks
            # to course objects and just serialize the entire course 
            tasks.append(task.serialize())

    return tasks
