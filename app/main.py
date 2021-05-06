import logging
import os
import time
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.logger import logger as fastapi_logger
from starlette.middleware.cors import CORSMiddleware
from api import events
from api.api import router as api_router
from api.settings import settings
from db import database

if "gunicorn" in os.environ.get("SERVER_SOFTWARE", ""):
    gunicorn_logger = logging.getLogger("gunicorn")
    gunicorn_logger.setLevel(logging.INFO)
    log_level = gunicorn_logger.level

    root_logger = logging.getLogger()
    gunicorn_error_logger = logging.getLogger("gunicorn.error")
    uvicorn_access_logger = logging.getLogger("uvicorn.access")

    # Use gunicorn error handlers for root, uvicorn, and fastapi loggers
    root_logger.handlers = gunicorn_error_logger.handlers
    uvicorn_access_logger.handlers = gunicorn_error_logger.handlers
    fastapi_logger.handlers = gunicorn_error_logger.handlers

    # Pass on logging levels for root, uvicorn, and fastapi loggers
    root_logger.setLevel(log_level)
    uvicorn_access_logger.setLevel(log_level)
    fastapi_logger.setLevel(log_level)


logger = logging.getLogger(__name__)

app = FastAPI(title='Tattoo API', description='Tattoo API to provide database functionality to booking software')


origins = [
    f"http://{settings.client_hostname}", 
    f"https://{settings.client_hostname}"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", origins],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

logger.info('add v1 endpoints..')
# add v1
app.include_router(api_router, prefix='/api')
app.add_event_handler('startup', events.startup_event_handler(app))
app.add_exception_handler(HTTPException, events.on_http_error)

@app.on_event("startup")
async def startup():
    time.sleep(3)
    try:
        await database.connect()
    except BaseException:
        time.sleep(3)
        await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()