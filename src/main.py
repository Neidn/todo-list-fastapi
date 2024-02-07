"""
main.py
"""
from fastapi.applications import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from .core.exception_handlers import http_exception_handler, validation_exception_handler


def create_app() -> FastAPI:
    """ app factory method """
    app = FastAPI()

    app.add_exception_handler(
        RequestValidationError,
        handler=validation_exception_handler,
    )
    app.add_exception_handler(
        HTTPException,
        handler=http_exception_handler
    )

    return app
