from pydantic import BaseModel

class ScrapeRequest(BaseModel):
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
    members: list
    meeting_blocks: list

class JoinClubRequest(BaseModel):
    user_id: str
    club_name: str