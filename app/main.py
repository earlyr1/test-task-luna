from fastapi import Depends, FastAPI

from app.deps import verify_api_key
from app.middlewares import JSONWrapperMiddleware
from app.routers import activities_router, organizations_router


def create_app(debug=False) -> FastAPI:
    app = FastAPI(debug=debug)

    app.add_middleware(JSONWrapperMiddleware)

    app.include_router(
        organizations_router, prefix="/orgs", dependencies=[Depends(verify_api_key)]
    )
    app.include_router(
        activities_router, prefix="/activities", dependencies=[Depends(verify_api_key)]
    )

    return app


app = create_app()


@app.get("/")
async def root():
    return {"status": "ok"}
