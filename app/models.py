from geoalchemy2 import Geography
from sqlalchemy import (ARRAY, BigInteger, ForeignKey, Index, Text,
                        UniqueConstraint, select)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class BaseModelWithId(Base):

    __abstract__ = True
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    @classmethod
    async def get_by_id(
        cls,
        session: AsyncSession,
        obj_id: int,
    ):
        stmt = select(cls).where(cls.id == obj_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()


class Building(BaseModelWithId):
    __tablename__ = "buildings"

    address: Mapped[str] = mapped_column(Text, nullable=False)
    location: Mapped[str] = mapped_column(
        Geography(geometry_type="POINT", srid=4326), nullable=False
    )

    organizations = relationship("Organization", back_populates="building")

    __table_args__ = (
        Index("idx_buildings_location", "location", postgresql_using="gist"),
    )


class Organization(BaseModelWithId):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(Text, nullable=False)
    phone_numbers: Mapped[list[str]] = mapped_column(ARRAY(Text))
    building_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("buildings.id"), nullable=False
    )

    building = relationship("Building", back_populates="organizations")
    activities = relationship("OrgXActivity", back_populates="organization")

    __table_args__ = (
        Index("idx_org_name_hash", "name", postgresql_using="hash"),
        Index("idx_org_building", "building_id"),
    )


class Activity(BaseModelWithId):
    __tablename__ = "activity"

    parent_activity_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("activity.id"), nullable=True
    )
    name: Mapped[str] = mapped_column(Text, nullable=False)

    parent = relationship("Activity", remote_side="Activity.id")
    organizations = relationship("OrgXActivity", back_populates="activity")


class OrgXActivity(BaseModelWithId):
    __tablename__ = "org_x_activities"

    org_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    activity_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("activity.id", ondelete="CASCADE"), nullable=False
    )

    organization = relationship("Organization", back_populates="activities")
    activity = relationship("Activity", back_populates="organizations")

    __table_args__ = (
        UniqueConstraint("org_id", "activity_id", name="uq_org_activity"),
        Index("idx_org_x_activities_org_id", "org_id"),
        Index("idx_org_x_activities_activity_id", "activity_id"),
    )
