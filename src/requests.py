from pydantic import BaseModel

class ScrapeRequest(BaseModel):
    user_id: int
    platform_code: str
    auth_token: str

class LinkRequest(BaseModel):
    user_id: int
    auth_token: str
    platform_code: str
    username: str
    password: str
