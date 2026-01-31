from fastapi import APIRouter, Depends
from pydantic import BaseModel as BaseSchema
from pydantic import ConfigDict

from app.controllers import ActivityController
from app.deps import get_activity_controller, verify_api_key

router = APIRouter(dependencies=[Depends(verify_api_key)])


class ActivitySchema(BaseSchema):
    name: str
    id: int
    parent_activity_id: int | None = None

    model_config = ConfigDict(from_attributes=True)


@router.get("", response_model=list[ActivitySchema])
async def get_activities(
    activity_controller: ActivityController = Depends(get_activity_controller),
):
    activities_list = await activity_controller.get_all_activities()
    return activities_list
