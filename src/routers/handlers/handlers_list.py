from app import app
from core.exceptions import auth_exceptions, event_exceptions, external_exceptions, parlay_exceptions
from routers.handlers import (
    auth_errors_handlers,
    event_errors_handlers,
    external_errors_handlers,
    parlay_errors_handlers,
)

# external exceptions
app.add_exception_handler(external_exceptions.ExternalException, external_errors_handlers.external_exception_handler)

# auth exceptions
app.add_exception_handler(auth_exceptions.InvalidJwtToken, auth_errors_handlers.invalid_jwt_token_handler)
app.add_exception_handler(auth_exceptions.NotAuthorizedException, auth_errors_handlers.not_authorized_exception_handler)

# parlay exceptions
app.add_exception_handler(
    parlay_exceptions.ParlayNotFoundException, parlay_errors_handlers.parlay_not_found_exception_handler
)

# event exceptions
app.add_exception_handler(
    event_exceptions.EventNotFoundException, event_errors_handlers.event_not_found_exception_handler
)
