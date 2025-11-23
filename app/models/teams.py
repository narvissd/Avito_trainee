from typing import Optional, Dict, List
from app.database.db import database
from app.database.models import teams, users
from sqlalchemy import select, insert, update


class Teams:
    @staticmethod
    async def get_by_name(team_name: str) -> Optional[Dict]:
        query_team = select(teams.c.name).where(teams.c.name == team_name)
        team = await database.fetch_one(query_team)

        if not team:
            return None

        query = select(users.c.id.label("user_id"), users.c.username, users.c.is_active).where(
            users.c.team_name == team_name)

        data = await database.fetch_all(query)

        return {
            "team_name": team["name"],
            "members": [dict(m) for m in data]
        }

    @staticmethod
    async def create(team_name: str, members: List) -> Optional[Dict]:
        query_check = select(teams.c.name).where(teams.c.name == team_name)
        existing_team = await database.fetch_one(query_check)

        if existing_team:
            return None

        await database.execute(insert(teams).values(name=team_name))

        for member in members:
            query_user = select(users.c.id).where(users.c.id == member.user_id)
            data_user = await database.fetch_one(query_user)

            user_data = {
                "id": member.user_id,
                "username": member.username,
                "team_name": team_name,
                "is_active": member.is_active
            }

            if data_user:
                await database.execute(
                    update(users).where(users.c.id == member.user_id).values(**user_data)
                )
            else:
                await database.execute(insert(users).values(**user_data))

        return {
            "team_name": team_name,
            "members": [m.dict() for m in members]
        }