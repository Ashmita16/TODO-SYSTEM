from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str
    description: str | None = None

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
    description: str | None = None
    is_completed: bool = False
    category_id: int

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    is_completed: bool | None = None
    category_id: int | None = None

class TodoResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    is_completed: bool
    category_id: int
    category: CategoryResponse

    class Config:
        from_attributes = True

class PaginatedTodoResponse(BaseModel):
    total: int
    page: int
    limit: int
    items: list[TodoResponse]