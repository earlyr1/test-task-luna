import pytest


@pytest.mark.asyncio
async def test_get_all_activities(client, activity):
    resp = await client.get("/activities")

    assert resp.status_code == 200
    data = resp.json()["content"]

    assert len(data) == 1
    assert data[0]["id"] == activity.id
    assert data[0]["name"] == "Food"
