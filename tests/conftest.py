import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.pool import NullPool

from app.config import settings
from app.deps import get_db
from app.main import create_app

TEST_DATABASE_URL = settings.DATABASE_URL

pytest_plugins = ["tests.fixtures"]

app = create_app(debug=True)


@pytest.fixture(scope="session")
def event_loop_policy():
    """Set event loop policy for the test session."""
    import asyncio

    return asyncio.get_event_loop_policy()


@pytest.fixture(scope="session")
def request_headers():
    return {
        settings.API_KEY_HEADER_NAME: settings.API_KEY,
    }


@pytest_asyncio.fixture(scope="function")
async def engine():
    """Create a test database engine and run migrations."""
    test_engine = create_async_engine(
        TEST_DATABASE_URL,
        poolclass=NullPool,
        echo=False,
    )
    yield test_engine
    await test_engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(engine):
    """Create a test database session."""
    async_session_maker = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session_maker() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture(scope="function")
async def client(db_session, request_headers):
    """Create a test client with overridden database dependency."""

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app, raise_app_exceptions=True),
        base_url="http://test",
        headers=request_headers,
    ) as test_client:
        yield test_client

    app.dependency_overrides.clear()
