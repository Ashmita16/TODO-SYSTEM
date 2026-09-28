from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_serializer

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_completed: bool = False
    category_id: int

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[str] = None
    category_id: Optional[int] = None

class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    is_completed: bool
    category_id: int
    category: CategoryResponse
    created_at: datetime
    updated_at: datetime

    @field_serializer("created_at", "updated_at")
    def serialize_dt(self, dt: datetime, _info) -> str:
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    class Config:
        from_attributes = True

class PaginatedTodoResponse(BaseModel):
    total: int
    page: int
    limit: int
    items: list[TodoResponse]