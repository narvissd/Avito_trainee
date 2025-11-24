from datetime import datetime
from typing import List, Optional

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
    mergedAt: Optional[datetime] = None


class PRResponse(BaseModel):
    pr: PullRequest


class PRMerge(BaseModel):
    pull_request_id: str


class PRReassign(BaseModel):
    pull_request_id: str
    old_user_id: str


class PRReassignResponse(BaseModel):
    pr: PullRequest
    replaced_by: str
