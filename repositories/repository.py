from sqlalchemy.orm import Session
from sqlalchemy import or_
from models.models import Category, Todo
from schemas.todo_schema import CategoryCreate, CategoryUpdate, TodoCreate, TodoUpdate

class CategoryRepository:
    def get_all(self, db: Session):
        return db.query(Category).all()

    def get_by_id(self, db: Session, category_id: int):
        return db.query(Category).filter(Category.id == category_id).first()

    def get_by_name(self, db: Session, name: str):
        return db.query(Category).filter(Category.name == name).first()

    def create(self, db: Session, schema: CategoryCreate):
        category = Category(name=schema.name, description=schema.description)
        db.add(category)
        db.commit()
        db.refresh(category)
        return category

    def update(self, db: Session, category: Category, schema: CategoryUpdate):
        category.name = schema.name
        category.description = schema.description
        db.commit()
        db.refresh(category)
        return category

    def delete(self, db: Session, category: Category):
        db.delete(category)
        db.commit()


class TodoRepository:
    def create(self, db: Session, schema: TodoCreate) -> Todo:
        todo = Todo(
            title=schema.title,
            description=schema.description,
            is_completed=schema.is_completed,
            category_id=schema.category_id,
        )
        db.add(todo)
        db.commit()
        db.refresh(todo)
        return todo

    def get_by_id(self, db: Session, todo_id: int) -> Todo | None:
        return db.query(Todo).filter(Todo.id == todo_id).first()

    def list_todos(
        self,
        db: Session,
        category_id: int | None = None,
        is_completed: bool | None = None,
        search: str | None = None,
        skip: int = 0,
        limit: int = 10,
    ) -> tuple[list[Todo], int]:
        query = db.query(Todo)

        if category_id is not None:
            query = query.filter(Todo.category_id == category_id)

        if is_completed is not None:
            query = query.filter(Todo.is_completed == is_completed)

        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                or_(
                    Todo.title.ilike(search_filter),
                    Todo.description.ilike(search_filter),
                )
            )

        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return items, total

    def update(self, db: Session, todo: Todo, schema: TodoUpdate) -> Todo:
        update_data = schema.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(todo, key, value)
        db.commit()
        db.refresh(todo)
        return todo

    def delete(self, db: Session, todo: Todo):
        db.delete(todo)
        db.commit()

    def delete_by_category_id(self, db: Session, category_id: int) -> int:
        deleted_count = db.query(Todo).filter(Todo.category_id == category_id).delete(synchronize_session=False)
        db.commit()
        return deleted_count