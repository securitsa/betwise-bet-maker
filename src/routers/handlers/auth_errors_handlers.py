from fastapi import Request, status
from fastapi.responses import JSONResponse

from core.exceptions.auth_exceptions import InvalidJwtToken, NotAuthorizedException


async def invalid_jwt_token_handler(request: Request, exc: InvalidJwtToken):
    return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "Invalid JWT Token"})


async def not_authorized_exception_handler(request: Request, exc: NotAuthorizedException):
    return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={f"detail": f"Operation is not permitted"})
