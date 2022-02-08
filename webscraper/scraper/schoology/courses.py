# returns schoology course api output into course objects

# imports
import uuid

# local import
from webscraper.models import Course

# parses schoology given course information into SchoolVerse course objects
def parse_courses(courses_json) -> list:

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