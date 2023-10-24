from routers import healthcheck
from routers.handlers.handlers_list import app
from routers.v1.events import events
from routers.v1.me import parlays_statistics
from routers.v1.parlay import parlay
from routers.v1.parlays import parlays

app.include_router(healthcheck.router, tags=["Healthcheck"])
app.include_router(parlay.router, tags=["Parlay"])
app.include_router(events.router, tags=["Events"])
app.include_router(parlays.router, tags=["Parlays"])
app.include_router(parlays_statistics.router, tags=["Parlays statistics"])
