# imports
import os
from random import betavariate 
import sys

# adding directories for local imports
parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentdir)
currentdir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(currentdir)

# external imports
from bs4 import BeautifulSoup

def parse_descriptions(tasks, schoology_session):
    s = schoology_session

    for task in tasks:

        code = task['platform_information']['assignment_code']

        description_link = f"https://hackley.schoology.com/assignment/{code}/info"
        response = s.get(description_link)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')

        description_container = soup.find_all('div', {'class':"info-body"})
        if len(description_container) == 0:
            continue
        else:
            description_container = description_container[0]

        description = ''''''
        for section in description_container.contents:
            if section.name == 'p':
                try:
                    p_contents = section.string
                except:
                    try:
                        p_contents = section.contents[0].string
                    except:
                        p_contents = section.contents[0].contents[0].string

                description = description + p_contents + "\n"
            
            elif section.name == 'ul':
                list_elements = section.contents
                for list_element in list_elements:
                    description = description + f"  {list_element.string}" + "\n"

        task['description'] = description

    return tasks
        

