# object-oriented representation of web-scraper view of firebase models
# these are only guidelines to accelerate the scraping process, and ensuring the JSON contains all required data
# considering firebase is noSQL, these can be modified at anytime

# These are also NOT representitive of the actual firebase models
# Instead, they are strictly to contain web-scraper related information

# todo #
# - standerize date formatting
# - deal with description attribute
# - all tasks need to have a course connection attribute
# - optional note in task? like added information that a student can type

# task object
# core of the project, contains information on an assignment
class Task():
   
    # attributes
    def __init__(self, id, name, due_date, completed, platform_information=None, description=None):
        
        # basic information
        self.id = id # SchoolVerse generate id for database storage
        self.name = name # Name of the task
        self.due_date = due_date # Unformatted date to be changed to format
        
        # platform connection
        self.platform_information = platform_information
        # stores connection in a dictionary with a platform code and a assignment code. 
        '''
            {
                'platform_code' : 'sc',
                'assignment_code' : 51025015
            }
        '''

        # storing checkmarks as boolean
        self.completed = completed

        # optionals
        self.description = description # stores an optional extended description for the assignment

    # serialize task object to dictionary that represents JSON
    def serialize(self):
        # adding ensured data 
        serialized_task = {
            'id' : self.id,
            'name' : self.name,
            'due_date' : self.due_date,
            'completed' : self.completed
        }

        #optionals
        if self.platform_information is not None:
            serialized_task['plaform_information'] = self.platform_information
        if self.description is not None:
            serialized_task['description'] = self.description

        return serialized_task

# course object
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
            'section' : self.section
        }

        # optionals 
        if self.platform_information is not None:
            serialized_course['platform_information'] = self.platform_information
        if self.tasks is not None:
            serialized_course['tasks'] = self.tasks

        return serialized_course