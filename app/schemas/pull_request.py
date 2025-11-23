from typing import List
from pydantic import BaseModel

class PRCreate(BaseModel):
    pull_request_id: str
    pull_request_name: str
    author_id: str

class PullRequest(BaseModel):
    pull_request_id: str
    pull_request_name: str
    author_id: str
    status: str
    assigned_reviewers: List[str]

class PRResponse(BaseModel):
    pr: PullRequest