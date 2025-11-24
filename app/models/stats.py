from typing import Dict
from app.database.db import database
from app.database.models import pull_requests, pr_reviewers
from sqlalchemy import select, func, desc


class Stats:
    @staticmethod
    async def get_stats() -> Dict:
        query = (select(pull_requests.c.status, func.count().label("count")).group_by(pull_requests.c.status))
        data = await database.fetch_all(query)

        open_count = 0
        merge_count = 0
        for row in data:
            if row["status"] == "OPEN":
                open_count = row["count"]
            elif row["status"] == "MERGED":
                merge_count = row["count"]

        query_top = (
            select(pr_reviewers.c.user_id, func.count().label("count")).group_by(pr_reviewers.c.user_id).order_by(
                desc("count")).limit(5))
        data_rv = await database.fetch_all(query_top)

        return {
            "total_pull_requests": open_count + merge_count,
            "pull_requests_open": open_count,
            "pull_requests_merged": merge_count,
            "top_reviewers": [
                {"user_id": rv["user_id"], "review_count": rv["count"]}
                for rv in data_rv
            ]
        }
