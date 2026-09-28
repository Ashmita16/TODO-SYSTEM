from typing import Any

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    code: str
    message: str
    detail: dict[str, Any]


class ValidationErrorDetail(BaseModel):
    location: list[Any]
    message: str
    type: str


class ValidationErrorResponse(BaseModel):
    code: str
    message: str
    detail: list[ValidationErrorDetail]