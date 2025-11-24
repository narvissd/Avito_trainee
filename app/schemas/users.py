from typing import List

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


class PullRequestShort(BaseModel):
    pull_request_id: str
    pull_request_name: str
    author_id: str
    status: str


class UserReviewsResponse(BaseModel):
    user_id: str
    pull_requests: List[PullRequestShort]
