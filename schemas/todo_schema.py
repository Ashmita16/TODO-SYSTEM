from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_serializer


class TodoCreate(BaseModel):
    title: str
    description: str | None = None
    category_id: int
    is_completed: bool = False


class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    category_id: int | None = None
    is_completed: bool | None = None


class TodoResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    is_completed: bool
    category_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("created_at", "updated_at")
    def format_datetime(self, value: datetime) -> str:
        return value.strftime("%d-%m-%Y %H:%M:%S")


class PaginatedTodoResponse(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int
    items: list[TodoResponse]

    model_config = ConfigDict(from_attributes=True)