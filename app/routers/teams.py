from fastapi import APIRouter, HTTPException, status
from app.schemas.teams import Team
from app.models.teams import Teams

teams_router = APIRouter()


@teams_router.get("/team/get", response_model=Team)
async def get_team(team_name: str):
    data = await Teams.get_by_name(team_name)
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "NOT_FOUND", "message": "Team not found"}})
    return data


@teams_router.post("/team/add", response_model=Team, status_code=status.HTTP_201_CREATED)
async def create_team(team: Team):
    result = await Teams.create(team.team_name, team.members)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": {"code": "TEAM_EXISTS", "message": "team_name already exists"}})

    return result