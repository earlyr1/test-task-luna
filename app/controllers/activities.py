from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Activity


class ActivityController:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_activities(self) -> list[Activity]:
        stmt = select(Activity)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())
