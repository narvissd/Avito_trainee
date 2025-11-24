from fastapi import APIRouter

from app.models.stats import Stats
from app.schemas.stats import StatsResponse

stats_router = APIRouter()


@stats_router.get("/stats", response_model=StatsResponse)
async def get_stats():
    return await Stats.get_stats()
