from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from middleware.logging import LoggingMiddleware
from api import user, category, todo

from errors.exception import AppError
from errors.handlers import (
    app_error_handler,
    validation_error_handler,
    internal_server_error_handler
)


app = FastAPI(
    title="TODO MANAGEMENT SYSTEM",
    version="1.0.0",
)


app.add_middleware(LoggingMiddleware)


app.include_router(user.router)
app.include_router(category.router)
app.include_router(todo.router)


app.add_exception_handler(
    AppError,
    app_error_handler
)

app.add_exception_handler(
    RequestValidationError,
    validation_error_handler
)

app.add_exception_handler(
    Exception,
    internal_server_error_handler
)


@app.get("/", tags=["Health Check"])
def root():
    return {
        "message": "TODO MANAGEMENT SYSTEM IS RUNNING SUCCESSFULLY!"
    }