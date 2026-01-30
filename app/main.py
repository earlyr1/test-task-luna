from fastapi import FastAPI

from app.middlewares import ApiKeyMiddleware, JSONWrapperMiddleware
from app.routers import organizations_router


def create_app(debug=False) -> FastAPI:
    app = FastAPI(debug=debug)

    app.add_middleware(ApiKeyMiddleware)
    app.add_middleware(JSONWrapperMiddleware)

    app.include_router(organizations_router, prefix="/orgs")

    return app


app = create_app()


@app.get("/")
async def root():
    return {"status": "ok"}
