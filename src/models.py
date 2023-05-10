import uuid
from datetime import datetime

class Task():
   
    def __init__(self, name, due_date, course_id=None, course_name=None, completed=False, platform_information=None, description=None):
    
        self.name = name 
        self.due_date = due_date # unformatted here, formatted when dumped to firebase
        
        self.course_id = course_id 
        self.course_name = course_name

        self.platform_information = platform_information
        # stores connection in a dictionary with a platform code and a assignment code. 
        '''
            {
                'platform_code' : 'sc',
                'assignment_code' : 51025015
            }
        '''

        self.completed = completed # default to false
        self.description = description # optional extended description

    def serialize(self):
        
        serialized_task = {
            'name' : self.name,
            'due_date' : self.due_date,
            'completed' : self.completed
        }

        #optionals
        if self.platform_information is not None:
            serialized_task['platform_information'] = self.platform_information
        if self.description is not None:
            serialized_task['description'] = self.description
        if self.course_id is not None:
            serialized_task['course_id'] = self.course_id
        if self.course_name is not None:
            serialized_task['course_name'] = self.course_name

        return serialized_task

class Course():

    def __init__(self, id, name, section, platform_information=None, tasks=None):

        self.id = id
        self.name = name
        self.section = section

        self.platform_information = platform_information
        # platform information looks like this:
        '''
            {
                'platform_code' : 'sc',
                'course_code' : 41240140
            }
        '''

        # optionals 
        self.tasks= tasks # an array of task objects that are related to this course object

    def serialize(self):
        
        serialized_course = {
            'id' : self.id,
            'name' : self.name,
            'section' : self.section,
        }

        # optionals 
        if self.platform_information is not None:
            serialized_course['platform_information'] = self.platform_information
        if self.tasks is not None:
            serialized_course['tasks'] = self.tasks

        return serialized_course

# event object, like "winter break today" for example
class Event():

    def __init__(self, id, name, location, description, start_date, start_time, end_date, end_time, platform_information=None):
        self.id = id
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.start_time = start_time
        self.end_time = end_time
        self.location = location
        self.description = description

        self.platform_information = platform_information

    def serialize(self):
        serialized_event = {
            'id' : self.id,
            'name' : self.name,
            'start_date' : self.start_date,
            'end_date' : self.end_date,
            'start_time' : self.start_time,
            'end_time' : self.end_time,
            'location' : self.location,
            'description' : self.description
        }

        if self.platform_information is not None:
            serialized_event['platform_information'] = self.platform_information

        return serialized_event

class User():

    def __init__(self, id, credentials, courses=None):
        self.id = id,
        self.courses = courses
        self.credentials = credentials # as a dict with platform code as key and {"username": username, "password": password} as value

    def serialize(self):
        serialized_user = {
            "id" : self.id,
            "credentials" : self.credentials
        }

        #optionals
        if self.courses is not None:
            serialized_user['courses'] = self.courses

        return serialized_user

class Temp_Event:
    def __init__(self, id, name, due_date, course_name, course_id):
        self.name = name
        self.due_date = due_date
        self.id = id
        self.course_name = course_name
        self.course_id = course_id
        self.completed = False

        self.platform_information = {
            'platform_code' : 'sc',
            'assignment_code' : id
        }

        self.task = Task(name, due_date, platform_information=self.platform_information)

    def serialize(self):
        return {
            'name': self.name,
            'due_date': self.due_date,
            'course_name': self.course_name,
            'course_id': self.course_id,
            'platform_information': self.platform_information,
            'completed': self.completed,
            'description': ''
        }

# day, month two digits (ex. 01) year four digits (ex. 2020)
class SportModel:
    def __init__(self, id, start_date, start_time, end_date, end_time, description, location, link_style):
        self.id = uuid.uuid4()

        self.platform_information = {
            'platform_code': 'vc',
            'id': id,
            'link_style': link_style
        }

        self.location = location
        self.description = description
        
        self.start_date = convert_date(start_date, start_time)
        self.end_date = convert_date(end_date, end_time)

    def serialize(self):
        return {
            'id': str(self.id),
            'platform_information': self.platform_information,
            'location': self.location,
            'description': self.description,
            'start_date': self.start_date,
            'end_date': self.end_date
        }

def convert_date(date, time):

    if date is None:
        return None
    
    date = date.split("/")
    
    month = date[0]
    day = str(int(date[1]) + 1) # bug where dates are off by one
    year = date[2]

    if time is None:
        return datetime(int(year), int(month), int(day))

    times = time.split(" ")
    
    time = times[0].split(":")
    hour = time[0]
    minute = time[1]

    am_pm = times[1]
    if am_pm == "PM" and hour != "12":
        hour = int(hour) + 12

    date_object = datetime(int(year), int(month), int(day), int(hour), int(minute))
    
    return date_object

class ClubModel():
    def __init__(self, id, name, description, leader_ids, member_ids, meeting_blocks, meeting_block_style, group_notice, status):
        self.id = id
        self.name = name
        self.description = description
        self.leader_ids = leader_ids
        self.member_ids = member_ids
        self.meeting_blocks = meeting_blocks
        self.meeting_block_style = meeting_block_style, # OPTIONS BLOCK or TIME, for example "ddddTHH:mm:ss/ddddTHH:mm:ss" ie. "MondayT12:00:00/MondayT13:00:00" or "D#P#" where # is a number
        self.group_notice = group_notice
        self.status = False

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'leader_ids': self.leader_ids,
            'member_ids': self.member_ids,
            'meeting_blocks': self.meeting_blocks,
            'meeting_block_style': self.meeting_block_style,
            'group_notice': self.group_notice,
            'status': self.status
        }
    