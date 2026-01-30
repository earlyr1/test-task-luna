import pytest
from geoalchemy2.shape import from_shape
from shapely.geometry import Point

from app.models import Activity, Building, Organization, OrgXActivity


@pytest.fixture
async def building(db_session):
    building = Building(
        address="Test street 1",
        location=from_shape(Point(37.62, 55.75), srid=4326),
    )
    db_session.add(building)
    await db_session.flush()
    return building


@pytest.fixture
async def organization(db_session, building):
    org = Organization(
        name="Test Org",
        phone_numbers=["123", "456"],
        building_id=building.id,
    )
    db_session.add(org)
    await db_session.flush()
    return org


@pytest.fixture
async def activity(db_session):
    act = Activity(name="Food")
    db_session.add(act)
    await db_session.flush()
    return act


@pytest.fixture
async def org_activity(db_session, organization, activity):
    link = OrgXActivity(
        org_id=organization.id,
        activity_id=activity.id,
    )
    db_session.add(link)
    await db_session.flush()
    return link
