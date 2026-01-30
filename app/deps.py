from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

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


def get_organization_controller(
    db: AsyncSession = Depends(get_db),
) -> OrganizationController:
    return OrganizationController(db)


def get_activity_controller(
    db: AsyncSession = Depends(get_db),
) -> ActivityController:
    return ActivityController(db)
