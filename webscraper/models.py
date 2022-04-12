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

