import random
from typing import Dict, Union
from app.database.db import database
from app.database.models import pull_requests, pr_reviewers, users
from sqlalchemy import select, insert


class PullRequests:
    @staticmethod
    async def create(pr_id: str, name: str, author_id: str) -> Union[Dict, str]:
        query_pr = select(pull_requests.c.id).where(pull_requests.c.id == pr_id)
        if await database.fetch_one(query_pr):
            return "PR_EXISTS"

        query_author = select(users.c.team_name).where(users.c.id == author_id)
        data_author = await database.fetch_one(query_author)

        if not data_author:
            return "AUTHOR_NOT_FOUND"

        team_name = data_author["team_name"]

        query_candidates = select(users.c.id).where(users.c.team_name == team_name, users.c.is_active == True,
                                                    users.c.id != author_id)
        data_candidates = await database.fetch_all(query_candidates)
        candidates_ids = [row["id"] for row in data_candidates]

        count_candidates = min(len(candidates_ids), 2)
        assigned_reviewers = random.sample(candidates_ids, count_candidates)

        await database.execute(insert(pull_requests).values(
            id=pr_id,
            name=name,
            author_id=author_id,
            status="OPEN"
        ))

        if assigned_reviewers:
            reviewers_data = [{"pull_request_id": pr_id, "user_id": r_id} for r_id in assigned_reviewers]
            await database.execute(insert(pr_reviewers).values(reviewers_data))

        return {
            "pull_request_id": pr_id,
            "pull_request_name": name,
            "author_id": author_id,
            "status": "OPEN",
            "assigned_reviewers": assigned_reviewers
        }
