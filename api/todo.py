# from fastapi import APIRouter, Depends, status, Query
# from sqlalchemy.orm import Session
# from dependencies.db_dependency import get_db
# from schemas.todo_schema import TodoCreate, TodoUpdate, TodoResponse, PaginatedTodoResponse
# from services.services import TodoService

# router = APIRouter(prefix="/api/todos", tags=["Todos"])
# todo_service = TodoService()

# @router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
# def create_todo(schema: TodoCreate, db: Session = Depends(get_db)):
#     return todo_service.create(db, schema)

# @router.get("/", response_model=PaginatedTodoResponse)
# def get_todos(
#     category_id: int | None = Query(None, description="Filter by Category ID"),
#     is_completed: bool | None = Query(None, description="Filter by Completion status"),
#     search: str | None = Query(None, description="Search in title or description"),
#     page: int = Query(1, ge=1, description="Page number"),
#     limit: int = Query(10, ge=1, le=100, description="Page size"),
#     db: Session = Depends(get_db),
# ):
#     return todo_service.list_todos(
#         db, category_id=category_id, is_completed=is_completed, search=search, page=page, limit=limit
#     )

# @router.get("/{todo_id}", response_model=TodoResponse)
# def get_todo(todo_id: int, db: Session = Depends(get_db)):
#     return todo_service.get_by_id(db, todo_id)

# @router.put("/{todo_id}", response_model=TodoResponse)
# def update_todo(todo_id: int, schema: TodoUpdate, db: Session = Depends(get_db)):
#     return todo_service.update(db, todo_id, schema)

# @router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_todo(todo_id: int, db: Session = Depends(get_db)):
#     todo_service.delete(db, todo_id)
#     return None

# @router.delete("/category/{category_id}", status_code=status.HTTP_200_OK)
# def delete_todos_by_category(category_id: int, db: Session = Depends(get_db)):
#     deleted_count = todo_service.delete_by_category(db, category_id)
#     return {"message": f"Successfully deleted {deleted_count} todo(s) belonging to category {category_id}"}

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from dependencies.db_dependency import get_db
from dependencies.user_dependency import get_current_user
from schemas.todo_schema import TodoCreate, TodoUpdate, TodoResponse, PaginatedTodoResponse
from services.services import TodoService
from models.user import User

router = APIRouter(prefix="/api/todos", tags=["Todos"])
todo_service = TodoService()

@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(
    schema: TodoCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return todo_service.create(db, schema, current_user.id)

@router.get("/", response_model=PaginatedTodoResponse)
def get_todos(
    category_id: int | None = Query(None, description="Filter by Category ID"),
    is_completed: bool | None = Query(None, description="Filter by Completion status"),
    search: str | None = Query(None, description="Search in title or description"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Page size"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return todo_service.list_todos(
        db, 
        user_id=current_user.id,
        category_id=category_id, 
        is_completed=is_completed, 
        search=search, 
        page=page, 
        limit=limit
    )

@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(
    todo_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return todo_service.get_by_id(db, todo_id, current_user.id)

@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int, 
    schema: TodoUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return todo_service.update(db, todo_id, schema, current_user.id)

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    todo_service.delete(db, todo_id, current_user.id)
    return None

@router.delete("/category/{category_id}", status_code=status.HTTP_200_OK)
def delete_todos_by_category(
    category_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deleted_count = todo_service.delete_by_category(db, category_id, current_user.id)
    return {"message": f"Successfully deleted {deleted_count} todo(s) belonging to category {category_id}"}