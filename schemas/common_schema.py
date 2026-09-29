from typing import Any

from pydantic import BaseModel, ConfigDict

from typing import Generic, TypeVar, Any
from pydantic import BaseModel

T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: T | None = None
    meta: Any | None = None

    model_config = ConfigDict(from_attributes=True)

class CategoryCreate(BaseModel):
    name: str
    description: str | None = None


class CategoryUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str | None

    model_config = ConfigDict(from_attributes=True)