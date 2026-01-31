from geoalchemy2 import Geometry
from sqlalchemy import cast, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased
from sqlalchemy.sql import func

from app.models import Activity, Building, Organization, OrgXActivity


class OrganizationController:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_organization_by_id(self, item_id: int) -> Organization | None:
        return await Organization.get_by_id(self.session, item_id)

    async def get_organizations_by_building(
        self, building_id: int
    ) -> list[Organization]:
        stmt = select(Organization).where(Organization.building_id == building_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_organizations_by_activity_id(
        self, activity_id: int
    ) -> list[Organization]:
        stmt = select(Organization).where(
            Organization.activities.any(activity_id=activity_id)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def search_organizations_in_radius(
        self,
        lat: float,
        lon: float,
        radius_meters: float,
    ) -> list[Organization]:
        point = func.ST_SetSRID(
            func.ST_MakePoint(lon, lat),
            4326,
        )
        stmt = (
            select(Organization)
            .join(Organization.building)
            .where(Building.location.ST_DWithin(func.Geography(point), radius_meters))
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def search_organizations_in_rectangle(
        self,
        lat_min: float,
        lon_min: float,
        lat_max: float,
        lon_max: float,
    ) -> list[Organization]:
        envelope = func.ST_MakeEnvelope(
            lon_min,
            lat_min,
            lon_max,
            lat_max,
            4326,
        )

        stmt = (
            select(Organization)
            .join(Organization.building)
            .where(
                func.ST_Intersects(
                    cast(Building.location, Geometry),  # ← ВАЖНО
                    envelope,
                )
            )
        )

        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def search_organizations_by_activity(
        self, activity_id: int
    ) -> list[Organization]:

        A0 = aliased(Activity)  # текущая активность
        A1 = aliased(Activity)  # родитель
        A2 = aliased(Activity)  # родитель родителя
        A3 = aliased(Activity)  # родитель родителя родителя

        stmt = (
            select(Organization)
            .join(OrgXActivity, OrgXActivity.org_id == Organization.id)
            .join(A0, or_(A0.id == OrgXActivity.activity_id, A0.id == activity_id))
            .outerjoin(A1, A0.parent_activity_id == A1.id)
            .outerjoin(A2, A1.parent_activity_id == A2.id)
            .outerjoin(A3, A2.parent_activity_id == A3.id)
            .where(
                or_(
                    OrgXActivity.activity_id == activity_id,
                    A1.id == activity_id,
                    A2.id == activity_id,
                    A3.id == activity_id,
                )
            )
            .distinct()
        )

        res = await self.session.execute(stmt)
        orgs = res.scalars().all()
        return list(orgs)

    async def search_organizations_by_name(self, name: str) -> list[Organization]:
        stmt = select(Organization).where(
            Organization.name.ilike(f"%{name}%")
        )  # no index used; case-insensitive
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
