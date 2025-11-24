import random
from typing import Dict, Union, Optional
from app.database.db import database
from app.database.models import pull_requests, pr_reviewers, users
from sqlalchemy import select, insert, update, func


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

    @staticmethod
    async def merge(pr_id: str) -> Optional[Dict]:
        query_pr = select(pull_requests.c.id,
                          pull_requests.c.name,
                          pull_requests.c.author_id,
                          pull_requests.c.status,
                          pull_requests.c.merged_at
                          ).where(pull_requests.c.id == pr_id)

        data_pr = await database.fetch_one(query_pr)

        if not data_pr:
            return None

        if data_pr["status"] == "MERGED":
            data_pr_update = data_pr
        else:
            query_update = (update(pull_requests).where(pull_requests.c.id == pr_id).values(status="MERGED",
                                                                                            merged_at=func.now()).returning(
                pull_requests.c.id,
                pull_requests.c.name,
                pull_requests.c.author_id,
                pull_requests.c.status,
                pull_requests.c.merged_at))
            data_pr_update = await database.fetch_one(query_update)

        merged_at = data_pr_update["merged_at"]
        if merged_at:
            merged_at = merged_at.replace(microsecond=0)

        query = select(pr_reviewers.c.user_id).where(pr_reviewers.c.pull_request_id == pr_id)
        data_reviewers = await database.fetch_all(query)
        reviewers_ids = [rev["user_id"] for rev in data_reviewers]

        return {
            "pull_request_id": data_pr_update["id"],
            "pull_request_name": data_pr_update["name"],
            "author_id": data_pr_update["author_id"],
            "status": data_pr_update["status"],
            "assigned_reviewers": reviewers_ids,
            "mergedAt": merged_at
        }
