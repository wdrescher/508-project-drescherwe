import logging

from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import UJSONResponse

from api.settings import settings

log = logging.getLogger(__name__)

startup_msg_fmt = """
 Tattoo API started with {settings.app_environment}
    """


async def on_http_error(request: Request, exc: HTTPException):
    if exc.status_code >= 500:
        # SentryAsgiMiddleware captures all exceptions, this is to keep track of
        # handled exceptions.
        capture_exception(exc)
    return UJSONResponse({'detail': exc.detail}, status_code=exc.status_code)


optional_services = []


async def on_startup(app):
    services_status = {}
    for name, env_var, initializer in optional_services:
        res = False
        if env_var:
            try:
                log.info('initializing \'%s\'..' % name)
                res = initializer(app)
            except:
                log.exception('failed to start \'%s\'.' % name)
        services_status[name] = res

    services_str = '\n\t'.join(['%s: %s' % (k, v) for k, v in services_status.items()])

    startup_msg = startup_msg_fmt.format(
        settings=settings, services=services_str
    )
    log.info(startup_msg)


def startup_event_handler(app):
    async def start_app() -> None:
        await on_startup(app)

    return start_app
