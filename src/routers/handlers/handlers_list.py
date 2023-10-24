from app import app
from core.exceptions import external_exceptions
from routers.handlers import external_errors_handlers

# external exceptions
app.add_exception_handler(external_exceptions.ExternalException, external_errors_handlers.external_exception_handler)
