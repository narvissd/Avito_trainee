from typing import Dict, Optional

from sqlalchemy import select, update

from app.database.db import database
from app.database.models import pr_reviewers, pull_requests, users


class Users:
    @staticmethod
    async def set_is_active(user_id: str, is_active: bool) -> Optional[Dict]:
        query_user = select(users).where(users.c.id == user_id)
        data_user = await database.fetch_one(query_user)

        if not data_user:
            return None

        query = update(users).where(users.c.id == user_id).values(is_active=is_active)
        await database.execute(query)

        return {
            "user_id": data_user["id"],
            "username": data_user["username"],
            "team_name": data_user["team_name"],
            "is_active": is_active,
        }

    @staticmethod
    async def get_reviews(user_id: str) -> Dict:
        query = (
            select(
                pull_requests.c.id.label("pull_request_id"),
                pull_requests.c.name.label("pull_request_name"),
                pull_requests.c.author_id,
                pull_requests.c.status,
            )
            .join(pr_reviewers, pull_requests.c.id == pr_reviewers.c.pull_request_id)
            .where(pr_reviewers.c.user_id == user_id)
        )

        data = await database.fetch_all(query)

        pr_list = [dict(row) for row in data]

        return {"user_id": user_id, "pull_requests": pr_list}
