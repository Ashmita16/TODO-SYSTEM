
from sqlalchemy.orm import Session
from sqlalchemy import or_

from models.models import Category, Todo
from schemas.common_schema import CategoryCreate, CategoryUpdate
from schemas.todo_schema import TodoCreate, TodoUpdate


class CategoryRepository:

    def get_all(self, db: Session):
        return db.query(Category).all()

    def get_by_id(
        self,
        db: Session,
        category_id: int
    ):
        return (
            db.query(Category)
            .filter(Category.id == category_id)
            .first()
        )

    def get_by_name(
        self,
        db: Session,
        name: str
    ):
        return (
            db.query(Category)
            .filter(Category.name == name)
            .first()
        )

    def create(
        self,
        db: Session,
        schema: CategoryCreate
    ):
        category = Category(
            name=schema.name,
            description=schema.description
        )

        db.add(category)
        db.commit()
        db.refresh(category)

        return category

    def update(
        self,
        db: Session,
        category: Category,
        schema: CategoryUpdate
    ):
        update_data = schema.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(category, key, value)

        db.commit()
        db.refresh(category)

        return category

    def delete(
        self,
        db: Session,
        category: Category
    ):
        db.delete(category)
        db.commit()


class TodoRepository:

    def create(
        self,
        db: Session,
        schema: TodoCreate,
        user_id: int
    ):
        todo = Todo(
            title=schema.title,
            description=schema.description,
            category_id=schema.category_id,
            is_completed=getattr(
                schema,
                "is_completed",
                False
            ),
            user_id=user_id
        )

        db.add(todo)
        db.commit()
        db.refresh(todo)

        return todo


    def get_by_id(
        self,
        db: Session,
        todo_id: int,
        user_id: int
    ) -> Todo | None:

        return (
            db.query(Todo)
            .filter(
                Todo.id == todo_id,
                Todo.user_id == user_id
            )
            .first()
        )

    def list_todos(
        self,
        db: Session,
        user_id: int,
        category_id: int | None = None,
        is_completed: bool | None = None,
        search: str | None = None,
        skip: int = 0,
        limit: int = 10,
        sort_order: str = "desc"
    ) -> tuple[list[Todo], int]:

        query = (
            db.query(Todo)
            .filter(Todo.user_id == user_id)
        )


        if category_id is not None:
            query = query.filter(
                Todo.category_id == category_id
            )

        if is_completed is not None:
            query = query.filter(
                Todo.is_completed == is_completed
            )

        if search:
            search_filter = f"%{search}%"

            query = query.filter(
                or_(
                    Todo.title.ilike(search_filter),
                    Todo.description.ilike(search_filter)
                )
            )

        if sort_order.lower() == "asc":
            query = query.order_by(Todo.created_at.asc())
        else:
            query = query.order_by(Todo.created_at.desc())


        total = query.count()

        items = (
            query
            .offset(skip)
            .limit(limit)
            .all()
        )

        return items, total

    def get_all_for_export(
        self,
        db: Session,
        user_id: int
    ) -> list[Todo]:

        return (
            db.query(Todo)
            .filter(Todo.user_id == user_id)
            .order_by(Todo.created_at.desc())
            .all()
        )

    def update(
        self,
        db: Session,
        todo: Todo,
        schema: TodoUpdate
    ) -> Todo:

        update_data = schema.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(todo, key, value)

        db.commit()
        db.refresh(todo)

        return todo

    def delete(
        self,
        db: Session,
        todo: Todo
    ):
        db.delete(todo)
        db.commit()


    def delete_by_category_id(
        self,
        db: Session,
        category_id: int,
        user_id: int
    ) -> int:

        deleted_count = (
            db.query(Todo)
            .filter(
                Todo.category_id == category_id,
                Todo.user_id == user_id
            )
            .delete(
                synchronize_session=False
            )
        )

        db.commit()

        return deleted_count