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
    leader_names: list

    class Config:
        schema_extra = {
            "example": {
                "name": "Cringe Club",
                "description": "Cringe club is a sad club that meets on Tuesdays and Thursdays during lunch.",
                "leader_ids": ["1234567890", "0987654321"],
                "leader_names" : ["Steven Hi", "Hi Steven"],
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
    leader_name: str

class CreateClubEventRequest(BaseModel):
    club_id: str
    title: str
    description: str
    start: str
    end: str
    location: str
    leader_id: str

    class Config:
        schema_extra = {
            "example": {
                "club_id" : "1234567890",
                "start": "2012-01-01 12:00:00",
                "end": "2012-01-01 13:00:00",
                "title" : "Cringe Club Meeting",
                "description" : "Meeting to discuss how cringe we are.",
                "location" : "Room 123",
                "leader_id" : "0987654321",
            }
        }

class UpdateClubEventRequest(BaseModel):
    club_id: str
    id: str
    title: str
    description: str
    start: str
    end: str
    location: str
    leader_id: str

class DeleteClubEventRequest(BaseModel):
    club_id: str
    id: str
    leader_id: str