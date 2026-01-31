import pytest


@pytest.mark.asyncio
async def test_get_organizations_by_building(client, building, organization):
    resp = await client.get(f"/orgs/buildings/{building.id}")

    assert resp.status_code == 200
    data = resp.json()["content"]

    assert len(data) == 1
    assert data[0]["id"] == organization.id


async def test_get_organizations_by_activity(
    client, activity, organization, org_activity
):
    resp = await client.get(f"/orgs/activities/{activity.id}")

    assert resp.status_code == 200
    data = resp.json()["content"]

    assert len(data) == 1
    assert data[0]["name"] == "Test Org"


async def test_get_organization_by_id(client, organization):
    resp = await client.get(f"/orgs/{organization.id}")
    assert resp.status_code == 200
    data = resp.json()["content"]

    assert data["id"] == organization.id
    assert data["name"] == "Test Org"


async def test_search_organizations_by_name(client, organization):
    resp = await client.get("/orgs/search/by-name", params={"name": "Test"})

    assert resp.status_code == 200
    data = resp.json()["content"]

    assert len(data) == 1
    assert data[0]["name"] == "Test Org"


async def test_search_organizations_in_radius(client, organization):
    resp = await client.get(
        "/orgs/search/radius",
        params={
            "lat": 55.75,
            "lon": 37.62,
            "radius": 500,
        },
    )
    assert resp.status_code == 200
    data = resp.json()["content"]
    assert len(data) == 1


async def test_search_organizations_in_rectangle(client, organization):
    resp = await client.get(
        "/orgs/search/rectangle",
        params={
            "lat_min": 55.70,
            "lon_min": 37.60,
            "lat_max": 55.80,
            "lon_max": 37.70,
        },
    )

    assert resp.status_code == 200
    data = resp.json()["content"]
    assert len(data) == 1


async def test_search_organizations_by_activity_tree(
    client, activity, organization, org_activity
):
    resp = await client.get(f"/orgs/search/activity/{activity.id}")
    assert resp.status_code == 200
    data = resp.json()["content"]
    assert len(data) == 1
