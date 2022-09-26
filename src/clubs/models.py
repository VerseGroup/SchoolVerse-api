import uuid

class Club():

    def __init__(self, name, description, meeting_blocks, leaders, members, events, meetings, updates):
        self.name = name
        self.description = description
        self.meeting_blocks = meeting_blocks
        self.leaders = leaders
        self.members = members
        self.id = str(uuid.uuid4())

        # refs
        self.events = events
        self.meetings = meetings
        self.updates = updates

    def add_members(self, member):
        self.members.append(member)
    
    def add_leader(self, leader):
        self.leaders.append(leader)

    def add_event(self, event):
        self.events.append(event)
    
    def add_meeting(self, meeting):
        self.meetings.append(meeting)

    def add_update(self, update):
        self.updates.append(update)

    def update_decription(self, description):
        self.description = description

    def update_meeting_blocks(self, meeting_blocks):
        self.meeting_blocks = meeting_blocks

    def serialize(self):
        return {
            "name" : self.name,
            "description" : self.description,
            "meeting_blocks" : self.meeting_blocks,
            "leaders" : self.leaders,
            "members" : self.members,
            "events" : self.events,
            "meetings" : self.meetings,
            "updates" : self.updates,
            "id" : self.id
        }

class Update():

    def __init__(self, club_id, date_posted, description, title, posted_by):
        self.club_id = club_id
        self.date_posted = date_posted
        self.description = description
        self.title = title
        self.posted_by = posted_by
        self.id = str(uuid.uuid4())

    def serialize(self):
        return {
            "club_id": self.club_id,
            "date_posted": self.date_posted,
            "description": self.description,
            "title": self.title,
            "posted_by": self.posted_by,
            "id": self.id
        }

class Meeting():

    def __init__(self, id, club_id, date, description, location, title, time):
        self.id = id
        self.club = club_id
        self.date = date
        self.description = description
        self.location = location
        self.title = title
        self.time = time

    def serialize(self):
        return {
            "club_id": self.club_id,
            "date": self.date,
            "description": self.description,
            "location": self.location,
            "title": self.title,
            "time": self.time,
            "id": self.id
        }

class Event():

        def __init__(self, id, club_id, meeting_block, date, description, location, title, time):
            self.club = club_id
            self.date = date
            self.meeting_block = meeting_block
            self.description = description
            self.location = location
            self.title = title
            self.time = time
    
        def serialize(self):
            return {
                "id": self.id,
                "club_id": self.club_id,
                "date": self.date,
                "description": self.description,
                "location": self.location,
                "title": self.title,
                "time": self.time,
                "meeting_block": self.meeting_block
            }