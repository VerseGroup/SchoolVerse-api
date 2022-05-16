from pydantic import BaseModel

class ScrapeRequest(BaseModel):
    user_id: str
    platform_code: str
    auth_token: str

class LinkRequest(BaseModel):
    user_id: str
    auth_token: str
    platform_code: str
    username: str
    password: str

class SignUpRequest(BaseModel):
    userid: str