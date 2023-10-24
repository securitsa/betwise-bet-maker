import logging.config

from fastapi import FastAPI

from core.config import settings

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

app = FastAPI(**settings.fastapi_kwargs)
