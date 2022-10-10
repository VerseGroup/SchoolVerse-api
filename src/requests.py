from pydantic import BaseModel

class ScrapeRequest(BaseModel):
    user_id: str
    e_username: str
    e_password: str
    #platform_code: str
    #auth_token: str

class EnsureRequest(BaseModel):
    user_id: str
    e_username: str
    e_password: str
    #platform_code: str
    #auth_token: str

class SignUpRequest(BaseModel):
    user_id: str

class CreateClubRequest(BaseModel):
    name: str
    description: str
    leaders: list
    meeting_blocks: list

class JoinClubRequest(BaseModel):
    user_id: str
    club_id: str

class LeaveClubRequest(BaseModel):
    user_id: str
    club_id: str

class UpdateClubRequest(BaseModel):
    field_to_update: str
    new_value: str
    user_id: str
    club_id: str

class JoinSportRequest(BaseModel):
    user_id: str
    sport_id: str

class LeaveSportRequest(BaseModel):
    user_id: str
    sport_id: str