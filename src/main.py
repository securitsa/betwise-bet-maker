import logging

from core.config import settings
from routers.routers_list import app

logger = logging.getLogger()

logger.info(f"The application `{app.title}` has been started with the following settings: {settings}")
