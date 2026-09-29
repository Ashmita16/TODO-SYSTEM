import json

from fastapi import (
    APIRouter,
    Depends,
    Query,
    status
)

from fastapi.responses import Response

from sqlalchemy.orm import Session

from dependencies.db_dependency import get_db
from dependencies.user_dependency import get_current_user

from schemas.common_schema import SuccessResponse

from schemas.todo_schema import (
    TodoCreate,
    TodoUpdate,
    TodoResponse
)

from services.services import TodoService
from models.user import User


router = APIRouter(
    prefix="/api/todos",
    tags=["Todos"]
)

todo_service = TodoService()


@router.post(
    "/",
    response_model=SuccessResponse[TodoResponse],
    status_code=status.HTTP_201_CREATED
)
def create_todo(
    schema: TodoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    todo = todo_service.create(
        db,
        schema,
        current_user.id
    )

    return {
        "success": True,
        "message": "Todo created successfully",
        "data": todo,
        "meta": None
    }


@router.get(
    "/",
    response_model=SuccessResponse[list[TodoResponse]]
)
def get_todos(
    category_id: int | None = Query(
        None,
        description="Filter by Category ID"
    ),
    is_completed: bool | None = Query(
        None,
        description="Filter by Completion status"
    ),
    search: str | None = Query(
        None,
        description="Search in title or description"
    ),
    page: int = Query(
        1,
        ge=1,
        description="Page number"
    ),
    limit: int = Query(
        10,
        ge=1,
        le=100,
        description="Page size"
    ),
    sort_order: str = Query(
        "desc",
        pattern="^(asc|desc)$",
        description="Sort by created date: asc or desc"
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    result = todo_service.list_todos(
        db,
        user_id=current_user.id,
        category_id=category_id,
        is_completed=is_completed,
        search=search,
        page=page,
        limit=limit,
        sort_order=sort_order
    )

    return {
        "success": True,
        "message": "Todos fetched successfully",
        "data": result["items"],
        "meta": {
            "page": result["page"],
            "limit": result["limit"],
            "total": result["total"],
            "total_pages": result["total_pages"]
        }
    }


# EXPORT TODOS
@router.get(
    "/export",
    response_class=Response
)
def export_todos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    todos = todo_service.get_all_for_export(
        db,
        current_user.id
    )

    todo_data = []

    for todo in todos:

        todo_data.append({
            "id": todo.id,
            "title": todo.title,
            "description": todo.description,
            "is_completed": todo.is_completed,
            "category_id": todo.category_id,
            "created_at": (
                todo.created_at.isoformat()
                if todo.created_at
                else None
            ),
            "updated_at": (
                todo.updated_at.isoformat()
                if todo.updated_at
                else None
            )
        })

    json_data = json.dumps(
        todo_data,
        indent=4
    )

    return Response(
        content=json_data,
        media_type="application/json",
        headers={
            "Content-Disposition":
                'attachment; filename="todos.json"'
        }
    )


# GET TODO BY ID
@router.get(
    "/{todo_id}",
    response_model=SuccessResponse[TodoResponse]
)
def get_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    todo = todo_service.get_by_id(
        db,
        todo_id,
        current_user.id
    )

    return {
        "success": True,
        "message": "Todo fetched successfully",
        "data": todo,
        "meta": None
    }


# UPDATE TODO
@router.put(
    "/{todo_id}",
    response_model=SuccessResponse[TodoResponse]
)
def update_todo(
    todo_id: int,
    schema: TodoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    todo = todo_service.update(
        db,
        todo_id,
        schema,
        current_user.id
    )

    return {
        "success": True,
        "message": "Todo updated successfully",
        "data": todo,
        "meta": None
    }


# DELETE TODO
@router.delete(
    "/{todo_id}",
    status_code=status.HTTP_200_OK,
    response_model=SuccessResponse[None]
)
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    todo_service.delete(
        db,
        todo_id,
        current_user.id
    )

    return {
        "success": True,
        "message": "Todo deleted successfully",
        "data": None,
        "meta": None
    }


# DELETE TODOS BY CATEGORY
@router.delete(
    "/category/{category_id}",
    status_code=status.HTTP_200_OK,
    response_model=SuccessResponse[dict]
)
def delete_todos_by_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    deleted_count = todo_service.delete_by_category(
        db,
        category_id,
        current_user.id
    )

    return {
        "success": True,
        "message": "Todos deleted successfully",
        "data": {
            "deleted_count": deleted_count
        },
        "meta": None
    }