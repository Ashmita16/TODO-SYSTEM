from sqlalchemy.orm import Session
from repositories.repository import CategoryRepository, TodoRepository
from schemas.todo_schema import CategoryCreate, CategoryUpdate, TodoCreate, TodoUpdate
from exceptions.user_exception import ResourceNotFoundException, DuplicateResourceException, ResourceInUseException
from models.models import Todo

class CategoryService:
    def __init__(self):
        self.category_repo = CategoryRepository()

    def get_all(self, db: Session):
        return self.category_repo.get_all(db)

    def get_by_id(self, db: Session, category_id: int):
        category = self.category_repo.get_by_id(db, category_id)
        if not category:
            raise ResourceNotFoundException(f"Category with ID {category_id} not found")
        return category

    def create(self, db: Session, schema: CategoryCreate):
        if self.category_repo.get_by_name(db, schema.name):
            raise DuplicateResourceException(f"Category with name '{schema.name}' already exists")
        return self.category_repo.create(db, schema)

    def update(self, db: Session, category_id: int, schema: CategoryUpdate):
        category = self.get_by_id(db, category_id)
        existing_name = self.category_repo.get_by_name(db, schema.name)
        if existing_name and existing_name.id != category_id:
            raise DuplicateResourceException(f"Category name '{schema.name}' is already taken")
        return self.category_repo.update(db, category, schema)

    def delete(self, db: Session, category_id: int, force_delete: bool = False):
        category = self.get_by_id(db, category_id)
        todos_count = db.query(Todo).filter(Todo.category_id == category_id).count()

        if todos_count > 0 and not force_delete:
            raise ResourceInUseException(
                f"Category has {todos_count} associated todo(s). Use force_delete=True to force delete."
            )

        if force_delete and todos_count > 0:
            db.query(Todo).filter(Todo.category_id == category_id).delete(synchronize_session=False)

        self.category_repo.delete(db, category)


class TodoService:
    def __init__(self):
        self.todo_repo = TodoRepository()
        self.category_repo = CategoryRepository()

    def create(self, db: Session, schema: TodoCreate):
        if not self.category_repo.get_by_id(db, schema.category_id):
            raise ResourceNotFoundException(f"Category with ID {schema.category_id} does not exist")
        return self.todo_repo.create(db, schema)

    def get_by_id(self, db: Session, todo_id: int):
        todo = self.todo_repo.get_by_id(db, todo_id)
        if not todo:
            raise ResourceNotFoundException(f"Todo with ID {todo_id} not found")
        return todo

    def list_todos(
        self,
        db: Session,
        category_id: int | None = None,
        is_completed: bool | None = None,
        search: str | None = None,
        page: int = 1,
        limit: int = 10,
    ):
        if category_id is not None and not self.category_repo.get_by_id(db, category_id):
            raise ResourceNotFoundException(f"Category with ID {category_id} does not exist")

        skip = (page - 1) * limit
        items, total = self.todo_repo.list_todos(
            db, category_id=category_id, is_completed=is_completed, search=search, skip=skip, limit=limit
        )
        return {"total": total, "page": page, "limit": limit, "items": items}

    def update(self, db: Session, todo_id: int, schema: TodoUpdate):
        todo = self.get_by_id(db, todo_id)
        if schema.category_id is not None and not self.category_repo.get_by_id(db, schema.category_id):
            raise ResourceNotFoundException(f"Category with ID {schema.category_id} does not exist")
        return self.todo_repo.update(db, todo, schema)

    def delete(self, db: Session, todo_id: int):
        todo = self.get_by_id(db, todo_id)
        self.todo_repo.delete(db, todo)

    def delete_by_category(self, db: Session, category_id: int):
        if not self.category_repo.get_by_id(db, category_id):
            raise ResourceNotFoundException(f"Category with ID {category_id} does not exist")
        return self.todo_repo.delete_by_category_id(db, category_id)