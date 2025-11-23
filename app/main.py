from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from app.database.db import database

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


@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "ok",
        "db_connected": database.is_connected,
        "env": "production"
    }