# holds information scraped
class Task():
   
    # attributes
    def __init__(self, name, due_date, course_id=None, course_name=None, completed=False, platform_information=None, description=None):
        
        # basic information
        self.name = name # Name of the task
        self.due_date = due_date # Unformatted date to be changed to format
        
        # course information
        self.course_id = course_id
        self.course_name = course_name

        # platform connection
        self.platform_information = platform_information
        # stores connection in a dictionary with a platform code and a assignment code. 
        '''
            {
                'platform_code' : 'sc',
                'assignment_code' : 51025015
            }
        '''

        # storing checkmarks as boolean, defaulted to false
        self.completed = completed

        # optionals
        self.description = description # stores an optional extended description for the assignment

    # serialize task object to dictionary that represents JSON
    def serialize(self):
        # adding ensured data 
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

# used to group and identify task objects
class Course():

    #attributes
    def __init__(self, id, name, section, platform_information=None, tasks=None):

        # basic information
        self.id = id
        self.name = name
        self.section = section

        # platform connection
        self.platform_information = platform_information
        # platform connection is important to ensure that assignments
        # already in firebase are not overwritten (we can do this by comparing
        # schoology assigned codes and our own ids)
        '''
            {
                'platform_code' : 'sc',
                'course_code' : 41240140
            }
        '''

        # optionals 
        self.tasks= tasks # an array of task objects that are related to this course object

    # serialize course object to dictionary that represents JSON
    def serialize(self):
        # adding ensured data
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

# User object to represent a client
class User():

    def __init__(self, id, credentials, courses=None):
        self.id = id,

        # array of course objects
        self.courses = courses

        # Holding user credentials
        self.credentials = credentials 
        # formatted as a json file (containing ciphertext)
        '''
        {
            "sc": [username, password],
            "gc": [username, password],
            "vc" : [username, password]
        }
        '''

    # serialize object to dict representing JSON
    def serialize(self):
        # ensured data
        serialized_user = {
            "id" : self.id,
            "credentials" : self.credentials
        }

        #optionals
        if self.courses is not None:
            serialized_user['courses'] = self.courses

        return serialized_user

