from pydantic import BaseModel

class ScrapeRequest(BaseModel):
    user_id: str
    e_username: str
    e_password: str
    api_key: str
    #platform_code: str
    #auth_token: str

class EnsureRequest(BaseModel):
    user_id: str
    e_username: str
    e_password: str
    api_key: str
    #platform_code: str
    #auth_token: str

class SignUpRequest(BaseModel):
    user_id: str
    api_key: str

class ApproveRequest(BaseModel):
    user_id: str
    version: str
    api_key: str

class JoinSportRequest(BaseModel):     
    user_id: str
    sport_id: str

class LeaveSportRequest(BaseModel):
    user_id: str
    sport_id: str

class DeleteUserRequest(BaseModel):
    user_id: str
    api_key: str

class NotificationRequest(BaseModel):
    user_id: str
    api_key: str

class CreateUserRequest(BaseModel):
    user_id: str
    email: str
    display_name: str
    grade_level: str
    api_key: str

class CreateClubRequest(BaseModel):
    name: str
    description: str
    leader_ids: list

    class Config:
        schema_extra = {
            "example": {
                "name": "Cringe Club",
                "description": "Cringe club is a sad club that meets on Tuesdays and Thursdays during lunch.",
                "leader_ids": ["1234567890", "0987654321"]
            }
        }

class JoinClubRequest(BaseModel):
    member_id: str
    club_id: str

class LeaveClubRequest(BaseModel):
    member_id: str
    club_id: str

class AnnounceClubRequest(BaseModel):
    club_id: str
    leader_id: str
    announcement: str

class CreateClubEventRequest(BaseModel):
    club_id: str
    name: str
    description: str
    start_date: str
    start_time: str
    end_date: str
    end_time: str
    location: str

    class Config:
        schema_extra = {
            "example": {
                "start_time" : "12:00:00", 
                "start_date" : "2021-01-01",
                "end_time" : "13:00:00",
                "end_date" : "2021-01-01",
                "name" : "Cringe Club Meeting",
                "description" : "Meeting to discuss how cringe we are.",
                "location" : "Room 123"
            }
        }

class UpdateClubEventRequest(BaseModel):
    club_id: str
    id: str
    name: str
    description: str
    start_date: str
    start_time: str
    end_date: str
    end_time: str
    location: str

class DeleteClubEventRequest(BaseModel):
    club_id: str
    id: str