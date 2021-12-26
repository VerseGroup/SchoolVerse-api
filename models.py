# object-oriented representation of our firebase models
# these are only guidelines to accelerate the scraping process, and ensuring the JSON contains all required data
# considering firebase is noSQL, these can be modified at anytime

# todo #
# - standerize date formatting
# - deal with description attribute
# - all tasks need to have a course attribute

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

    
