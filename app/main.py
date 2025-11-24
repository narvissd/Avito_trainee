from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from app.database.db import database

from app.routers.teams import teams_router
from app.routers.users import users_router
from app.routers.pull_request import pr_router
from app.routers.stats import stats_router

async def startup():
    print("Application is starting...")
    await database.connect()


async def shutdown():
    print("Application is shutting down...")
    await database.disconnect()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    await startup()
    yield
    await shutdown()


app = FastAPI(
    title="PR Reviewer Assignment Service",
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None,
    lifespan=lifespan,
)

app.include_router(teams_router)
app.include_router(users_router)
app.include_router(pr_router)
app.include_router(stats_router)