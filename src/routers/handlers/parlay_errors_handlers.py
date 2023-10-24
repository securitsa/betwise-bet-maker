from fastapi import Request, status
from fastapi.responses import JSONResponse

from core.exceptions.parlay_exceptions import ParlayNotFoundException


async def parlay_not_found_exception_handler(request: Request, exc: ParlayNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={f"detail": f"Parlay not found: {exc.parlay_token}"},
    )
