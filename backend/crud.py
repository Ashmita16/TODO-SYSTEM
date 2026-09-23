from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from .models import (
    CategoryModel,
    TodoModel
)

def create_category(db: Session, data):

    existing = (
        db.query(CategoryModel)
        .filter(
            CategoryModel.name.ilike(data.name)
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Category already exists"
        )

    category = CategoryModel(
        name=data.name,
        description=data.description
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


def get_categories(db: Session):

    return (
        db.query(CategoryModel)
        .order_by(CategoryModel.id)
        .all()
    )


def get_category(db: Session, category_id: int):

    category = (
        db.query(CategoryModel)
        .filter(
            CategoryModel.id == category_id
        )
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return category


def update_category(
    db: Session,
    category_id: int,
    data
):

    category = get_category(
        db,
        category_id
    )

    values = data.model_dump(
        exclude_unset=True
    )

    if "name" in values:

        existing = (
            db.query(CategoryModel)
            .filter(
                CategoryModel.name.ilike(
                    values["name"]
                ),
                CategoryModel.id != category_id
            )
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Category name already exists"
            )

    for key, value in values.items():
        setattr(
            category,
            key,
            value
        )

    category.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(category)

    return category


def delete_category(
    db: Session,
    category_id: int,
    cascade_delete: bool
):

    category = get_category(
        db,
        category_id
    )

    todos = (
        db.query(TodoModel)
        .filter(
            TodoModel.category_id == category_id
        )
        .all()
    )

    if todos and not cascade_delete:

        raise HTTPException(
            status_code=400,
            detail=(
                "Category has associated Todos. "
                "Use cascade_delete=true"
            )
        )

    deleted_count = len(todos)

    if cascade_delete:

        for todo in todos:
            db.delete(todo)

    db.delete(category)

    db.commit()

    return {
        "message": "Category deleted successfully",
        "deleted_todos": deleted_count
    }

def check_category(
    db: Session,
    category_id: int
):

    category = (
        db.query(CategoryModel)
        .filter(
            CategoryModel.id == category_id
        )
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return category


def create_todo(
    db: Session,
    data
):

    check_category(
        db,
        data.category_id
    )

    todo = TodoModel(
        **data.model_dump()
    )

    db.add(todo)
    db.commit()
    db.refresh(todo)

    return todo


def get_todo(
    db: Session,
    todo_id: int
):

    todo = (
        db.query(TodoModel)
        .filter(
            TodoModel.id == todo_id
        )
        .first()
    )

    if not todo:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    return todo


def get_todos(
    db: Session,
    is_completed=None,
    priority=None,
    status=None,
    category_id=None,
    search=None,
    skip=0,
    limit=10
):

    query = db.query(TodoModel)

    if is_completed is not None:

        query = query.filter(
            TodoModel.is_completed == is_completed
        )

    if priority is not None:

        query = query.filter(
            TodoModel.priority == priority
        )

    if status is not None:

        query = query.filter(
            TodoModel.status == status
        )

    if category_id is not None:

        check_category(
            db,
            category_id
        )

        query = query.filter(
            TodoModel.category_id == category_id
        )

    if search:

        search_value = f"%{search}%"

        query = query.filter(
            or_(
                TodoModel.title.ilike(
                    search_value
                ),
                TodoModel.description.ilike(
                    search_value
                )
            )
        )

    return (
        query
        .order_by(TodoModel.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_todos_by_category(
    db: Session,
    category_id: int
):

    check_category(
        db,
        category_id
    )

    return (
        db.query(TodoModel)
        .filter(
            TodoModel.category_id == category_id
        )
        .order_by(TodoModel.id)
        .all()
    )


def delete_todos_by_category(
    db: Session,
    category_id: int
):

    check_category(
        db,
        category_id
    )

    todos = (
        db.query(TodoModel)
        .filter(
            TodoModel.category_id == category_id
        )
        .all()
    )

    count = len(todos)

    for todo in todos:
        db.delete(todo)

    db.commit()

    return {
        "message": "Todos deleted successfully",
        "deleted_count": count
    }


def update_todo(
    db: Session,
    todo_id: int,
    data
):

    todo = get_todo(
        db,
        todo_id
    )

    values = data.model_dump(
        exclude_unset=True
    )

    if "category_id" in values:

        check_category(
            db,
            values["category_id"]
        )

    for key, value in values.items():

        setattr(
            todo,
            key,
            value
        )

    todo.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(todo)

    return todo


def delete_todo(
    db: Session,
    todo_id: int
):

    todo = get_todo(
        db,
        todo_id
    )

    db.delete(todo)
    db.commit()

    return {
        "message": "Todo deleted successfully"
    }