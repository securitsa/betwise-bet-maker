from fastapi import Request, status
from fastapi.responses import JSONResponse

from core.exceptions.external_exceptions import ExternalException


async def external_exception_handler(request: Request, exc: ExternalException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={f"detail": f"Something goes wrong. Try again"},
    )
