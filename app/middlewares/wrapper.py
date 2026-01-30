import json

from fastapi import Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class JSONWrapperMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)

            body = b""
            async for chunk in response.body_iterator:
                body += chunk

            data = json.loads(body) if body else None

            return JSONResponse(
                status_code=response.status_code,
                content={
                    "status": "ok",
                    "content": data,
                },
            )

        except HTTPException as exc:
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "status": "error",
                    "content": exc.detail,
                },
            )

        except Exception as exc:
            return JSONResponse(
                status_code=500,
                content={
                    "status": "error",
                    "content": exc.__str__(),
                },
            )
