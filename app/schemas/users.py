from pydantic import BaseModel

class UserUpdate(BaseModel):
    user_id: str
    is_active: bool

class User(BaseModel):
    user_id: str
    username: str
    team_name: str
    is_active: bool

class UserResponse(BaseModel):
    user: User