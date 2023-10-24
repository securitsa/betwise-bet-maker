from routers import healthcheck
from routers.handlers.handlers_list import app

app.include_router(healthcheck.router, tags=["Healthcheck"])
