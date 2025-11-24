from typing import List
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

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
    mergedAt: Optional[datetime] = None

class PRResponse(BaseModel):
    pr: PullRequest


class PRMerge(BaseModel):
    pull_request_id: str
