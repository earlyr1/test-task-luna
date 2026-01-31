from fastapi import FastAPI

from app.middlewares import JSONWrapperMiddleware
from app.routers import activities_router, organizations_router


def create_app(debug=False) -> FastAPI:
    app = FastAPI(debug=debug)

    app.add_middleware(JSONWrapperMiddleware)

    app.include_router(organizations_router, prefix="/orgs")
    app.include_router(activities_router, prefix="/activities")

    return app


app = create_app()


@app.get("/")
async def root():
    return {"status": "ok"}
