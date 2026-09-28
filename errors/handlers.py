from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from errors.exception import AppError


async def app_error_handler(
    request: Request,
    exc: AppError
):
    return JSONResponse(
        status_code=400,
        content={
            "code": exc.code,
            "message": exc.message,
            "detail": exc.detail
        }
    )


async def validation_error_handler(
    request: Request,
    exc: RequestValidationError
):
    errors = []

    for error in exc.errors():
        errors.append(
            {
                "location": list(error.get("loc", [])),
                "message": error.get("msg", ""),
                "type": error.get("type", "")
            }
        )

    return JSONResponse(
        status_code=422,
        content={
            "code": "VALIDATION_ERROR",
            "message": "Validation error",
            "detail": errors
        }
    )


async def internal_server_error_handler(
    request: Request,
    exc: Exception
):
    return JSONResponse(
        status_code=500,
        content={
            "code": "INTERNAL_SERVER_ERROR",
            "message": "Internal server error",
            "detail": {
                "message": "An unexpected error occurred"
            }
        }
    )