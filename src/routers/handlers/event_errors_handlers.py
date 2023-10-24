from fastapi import Request, status
from fastapi.responses import JSONResponse

from core.exceptions.event_exceptions import EventNotFoundException


async def event_not_found_exception_handler(request: Request, exc: EventNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={f"detail": f"Event not found: {exc.event_token}"},
    )
