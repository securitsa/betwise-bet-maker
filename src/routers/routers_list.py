from routers import healthcheck
from routers.handlers.handlers_list import app
from routers.v1.events import events
from routers.v1.parlay import parlay

app.include_router(healthcheck.router, tags=["Healthcheck"])
app.include_router(parlay.router, tags=["Parlay"])
app.include_router(events.router, tags=["Events"])
