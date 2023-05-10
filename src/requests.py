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
    meeting_blocks: list
    meeting_block_style: str
    leader_ids: list

    class Config:
        schema_extra = {
            "example": {
                "name": "Cringe Club",
                "description": "Cringe club is a sad club that meets on Tuesdays and Thursdays during lunch.",
                "meeting_blocks": ["D4P3", "D5P2"],
                "meeting_block_style": "TIME",
                "leader_ids": ["1234567890", "0987654321"]
            }
        }

class JoinClubRequest(BaseModel):
    member_id: str
    club_id: str

class LeaveClubRequest(BaseModel):
    member_id: str
    club_id: str