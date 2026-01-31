from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel as BaseSchema
from pydantic import ConfigDict

from app.controllers import OrganizationController
from app.deps import get_organization_controller, verify_api_key

router = APIRouter(dependencies=[Depends(verify_api_key)])


class OrganizationSchema(BaseSchema):
    id: int
    name: str
    phone_numbers: list[str]
    building_id: int

    model_config = ConfigDict(from_attributes=True)


@router.get("/buildings/{item_id}", response_model=list[OrganizationSchema] | None)
async def get_organizations_by_building(
    item_id: int,
    organization_controller: OrganizationController = Depends(
        get_organization_controller
    ),
):
    orgs_list = await organization_controller.get_organizations_by_building(item_id)
    return orgs_list


@router.get("/activities/{item_id}", response_model=list[OrganizationSchema] | None)
async def get_organizations_by_activity(
    item_id: int,
    organization_controller: OrganizationController = Depends(
        get_organization_controller
    ),
):
    orgs_list = await organization_controller.get_organizations_by_activity_id(item_id)
    return orgs_list


@router.get("/{item_id}", response_model=OrganizationSchema | None)
async def get_organization_by_id(
    item_id: int,
    organization_controller: OrganizationController = Depends(
        get_organization_controller
    ),
):
    org = await organization_controller.get_organization_by_id(item_id)
    return org


@router.get("/search/radius", response_model=list[OrganizationSchema] | None)
async def search_organizations_in_radius(
    lat: float = Query(...),
    lon: float = Query(...),
    radius: int = Query(..., description="meters"),
    organization_controller: OrganizationController = Depends(
        get_organization_controller
    ),
):
    orgs = await organization_controller.search_organizations_in_radius(
        lat, lon, radius
    )
    return orgs


@router.get("/search/rectangle", response_model=list[OrganizationSchema] | None)
async def search_organizations_in_rectangle(
    lat_min: float = Query(...),
    lon_min: float = Query(...),
    lat_max: float = Query(...),
    lon_max: float = Query(...),
    organization_controller: OrganizationController = Depends(
        get_organization_controller
    ),
):
    orgs = await organization_controller.search_organizations_in_rectangle(
        lat_min, lon_min, lat_max, lon_max
    )
    return orgs


@router.get(
    "/search/activity/{item_id}", response_model=list[OrganizationSchema] | None
)
async def search_organizations_by_activity_3_layers_down(
    item_id: int,
    organization_controller: OrganizationController = Depends(
        get_organization_controller
    ),
):
    orgs = await organization_controller.search_organizations_by_activity(item_id)
    return orgs


@router.get("/search/by-name", response_model=list[OrganizationSchema] | None)
async def search_organizations_by_name(
    name: str = Query(...),
    organization_controller: OrganizationController = Depends(
        get_organization_controller
    ),
):
    orgs = await organization_controller.search_organizations_by_name(name)
    return orgs
