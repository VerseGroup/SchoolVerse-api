# imports
import uuid
import os 
import sys

# adding directories for local imports
parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentdir)
currentdir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(currentdir)

# local import
from ...models import Course

# parses schoology given course information into SchoolVerse course objects
def parseCourses(courses_json):

    # isolating course from JSON
    course_array = (courses_json['data'])['courses']

    # array to hold returned objects
    course_object_array = []

    # iterating through JSON array of Schoology formatted courses
    for course in course_array:
        
        # pulling information
        name = course["courseTitle"]
        section = course["sectionTitle"]
        course_code = course["nid"]
        id = str(uuid.uuid4())

        # converting schoology_id into standerd platform information
        platform_information = {
            "code" : "sc",
            "course_code" : course_code
        }

        # writing information to a course object
        course_object = Course(id=id, name=name, section=section, platform_information=platform_information)

        # adding course object to array
        course_object_array.append(course_object)

    return course_object_array