from typing import List

from pydantic import BaseModel


class ReviewerStat(BaseModel):
    user_id: str
    review_count: int


class StatsResponse(BaseModel):
    total_pull_requests: int
    pull_requests_open: int
    pull_requests_merged: int
    top_reviewers: List[ReviewerStat]
