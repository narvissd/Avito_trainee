import pytest_asyncio
from databases import DatabaseURL
from databases.backends.sqlite import SQLiteBackend
from httpx import ASGITransport, AsyncClient
from sqlalchemy import create_engine

from app.database.db import database, metadata
from app.main import app

TEST_DATABASE_URL = "sqlite:///./test.db"

# Синхронный движок для создания таблиц
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})


@pytest_asyncio.fixture(scope="function")
async def client():
    if database.is_connected:
        await database.disconnect()

    database.url = DatabaseURL(TEST_DATABASE_URL)

    database._backend = SQLiteBackend(TEST_DATABASE_URL)

    metadata.create_all(engine)

    await database.connect()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    if database.is_connected:
        await database.disconnect()
    metadata.drop_all(engine)
