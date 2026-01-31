from typing import AsyncGenerator

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.controllers import ActivityController, OrganizationController
from app.db import AsyncSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def verify_api_key(
    api_key: str = Header(..., alias=settings.API_KEY_HEADER_NAME)
):
    if api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized or invalid API Key",
        )
    return api_key


def get_organization_controller(
    db: AsyncSession = Depends(get_db),
) -> OrganizationController:
    return OrganizationController(db)


def get_activity_controller(
    db: AsyncSession = Depends(get_db),
) -> ActivityController:
    return ActivityController(db)
