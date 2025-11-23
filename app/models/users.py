from typing import Optional, Dict
from app.database.db import database
from app.database.models import users
from sqlalchemy import select, update


class Users:
    @staticmethod
    async def set_is_active(user_id: str, is_active: bool) -> Optional[Dict]:
        query_user = select(users).where(users.c.id == user_id)
        data_user = await database.fetch_one(query_user)

        if not data_user:
            return None

        query = (update(users).where(users.c.id == user_id).values(is_active=is_active))
        await database.execute(query)

        return {
            "user_id": data_user["id"],
            "username": data_user["username"],
            "team_name": data_user["team_name"],
            "is_active": is_active
        }
