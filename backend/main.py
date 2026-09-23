
from datetime import datetime
from enum import Enum
from typing import List, Optional
from zoneinfo import ZoneInfo

from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum as SQLEnum,
    Float,
    ForeignKey,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Session,
    relationship,
    sessionmaker,
)

DATABASE_URL = "sqlite:///./todos.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


class Base(DeclarativeBase):
    pass


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

IST = ZoneInfo("Asia/Kolkata")


def current_time():
    return datetime.now(IST)

class PriorityEnum(str, Enum):

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class StatusEnum(str, Enum):

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ARCHIVED = "archived"

class CategoryModel(Base):

    __tablename__ = "categories"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    description = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=current_time
    )

    updated_at = Column(
        DateTime,
        default=current_time,
        onupdate=current_time
    )

    todos = relationship(
        "TodoModel",
        back_populates="category"
    )


class TodoModel(Base):

    __tablename__ = "todos"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String,
        nullable=False,
        index=True
    )

    description = Column(
        String,
        nullable=False
    )

    is_completed = Column(
        Boolean,
        default=False
    )

    status = Column(
        SQLEnum(StatusEnum),
        default=StatusEnum.PENDING
    )

    priority = Column(
        SQLEnum(PriorityEnum),
        default=PriorityEnum.MEDIUM
    )

    due_date = Column(
        DateTime,
        nullable=True
    )

    estimated_hours = Column(
        Float,
        nullable=True
    )

    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=current_time
    )

    updated_at = Column(
        DateTime,
        default=current_time,
        onupdate=current_time
    )

    category = relationship(
        "CategoryModel",
        back_populates="todos"
    )

Base.metadata.create_all(
    bind=engine
)

class CategoryCreate(BaseModel):

    name: str = Field(
        ...,
        min_length=2
    )

    description: str = Field(
        ...,
        min_length=1
    )


class CategoryUpdate(BaseModel):

    name: Optional[str] = Field(
        None,
        min_length=2
    )

    description: Optional[str] = None


class CategoryResponse(BaseModel):

    id: int
    name: str
    description: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TodoCreate(BaseModel):

    title: str = Field(
        ...,
        min_length=1
    )

    description: str = Field(
        ...,
        min_length=1
    )

    is_completed: bool = False

    status: StatusEnum = StatusEnum.PENDING

    priority: PriorityEnum = PriorityEnum.MEDIUM

    due_date: Optional[datetime] = None

    estimated_hours: Optional[float] = Field(
        None,
        ge=0
    )

    category_id: int


class TodoUpdate(BaseModel):

    title: Optional[str] = Field(
        None,
        min_length=1
    )

    description: Optional[str] = None

    is_completed: Optional[bool] = None

    status: Optional[StatusEnum] = None

    priority: Optional[PriorityEnum] = None

    due_date: Optional[datetime] = None

    estimated_hours: Optional[float] = Field(
        None,
        ge=0
    )

    category_id: Optional[int] = None


class TodoResponse(BaseModel):

    id: int
    title: str
    description: str
    is_completed: bool
    status: StatusEnum
    priority: PriorityEnum
    due_date: Optional[datetime]
    estimated_hours: Optional[float]
    category_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

app = FastAPI(
    title="TODO MANAGEMENT SYSTEM",
    version="1.0"
)

@app.get("/")
def home():

    return {
        "message": "TODO MANAGEMENT IS RUNNING"
    }

@app.post(
    "/categories",
    response_model=CategoryResponse,
    status_code=201
)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):

    existing_category = (
        db.query(CategoryModel)
        .filter(
            CategoryModel.name.ilike(
                category.name.strip()
            )
        )
        .first()
    )

    if existing_category:

        raise HTTPException(
            status_code=400,
            detail="Category already exists"
        )

    new_category = CategoryModel(
        name=category.name.strip(),
        description=category.description.strip()
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category

@app.get(
    "/categories",
    response_model=List[CategoryResponse]
)
def get_categories(
    db: Session = Depends(get_db)
):

    return (
        db.query(CategoryModel)
        .order_by(CategoryModel.id)
        .all()
    )

@app.get(
    "/categories/{category_id}",
    response_model=CategoryResponse
)
def get_category(
    category_id: int,
    db: Session = Depends(get_db)
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

@app.put(
    "/categories/{category_id}",
    response_model=CategoryResponse
)
def update_category(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db)
):

    db_category = (
        db.query(CategoryModel)
        .filter(
            CategoryModel.id == category_id
        )
        .first()
    )

    if not db_category:

        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    data = category.model_dump(
        exclude_unset=True
    )

    if "name" in data:

        existing_category = (
            db.query(CategoryModel)
            .filter(
                CategoryModel.name.ilike(
                    data["name"].strip()
                ),
                CategoryModel.id != category_id
            )
            .first()
        )

        if existing_category:

            raise HTTPException(
                status_code=400,
                detail="Category name already exists"
            )

        data["name"] = data["name"].strip()

    if "description" in data:

        data["description"] = (
            data["description"].strip()
        )

    for key, value in data.items():

        setattr(
            db_category,
            key,
            value
        )

    db_category.updated_at = current_time()

    db.commit()
    db.refresh(db_category)

    return db_category

@app.delete(
    "/categories/{category_id}"
)
def delete_category(
    category_id: int,
    cascade_delete: bool = Query(
        False,
        description="Delete associated Todos also"
    ),
    db: Session = Depends(get_db)
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

    todo_count = (
        db.query(TodoModel)
        .filter(
            TodoModel.category_id == category_id
        )
        .count()
    )

    if todo_count > 0 and not cascade_delete:

        raise HTTPException(
            status_code=400,
            detail=(
                "Category has associated Todos. "
                "Use cascade_delete=true"
            )
        )

    deleted_todos = 0

    if cascade_delete:

        deleted_todos = (
            db.query(TodoModel)
            .filter(
                TodoModel.category_id == category_id
            )
            .delete(
                synchronize_session=False
            )
        )

    db.delete(category)
    db.commit()

    return {
        "message": "Category deleted successfully",
        "deleted_todos": deleted_todos
    }

@app.post(
    "/todos",
    response_model=TodoResponse,
    status_code=201
)
def create_todo(
    todo: TodoCreate,
    db: Session = Depends(get_db)
):

    category = (
        db.query(CategoryModel)
        .filter(
            CategoryModel.id == todo.category_id
        )
        .first()
    )

    if not category:

        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    new_todo = TodoModel(
        title=todo.title.strip(),
        description=todo.description.strip(),
        is_completed=todo.is_completed,
        status=todo.status,
        priority=todo.priority,
        due_date=todo.due_date,
        estimated_hours=todo.estimated_hours,
        category_id=todo.category_id
    )

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return new_todo
@app.get(
    "/todos",
    response_model=List[TodoResponse]
)
def get_todos(
    is_completed: Optional[bool] = Query(
        None,
        description="Filter by completion"
    ),

    priority: Optional[PriorityEnum] = Query(
        None
    ),

    status: Optional[StatusEnum] = Query(
        None
    ),

    category_id: Optional[int] = Query(
        None
    ),

    search: Optional[str] = Query(
        None,
        description="Search title or description"
    ),

    skip: int = Query(
        0,
        ge=0
    ),

    limit: int = Query(
        10,
        ge=1,
        le=100
    ),

    db: Session = Depends(get_db)
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

        query = query.filter(
            TodoModel.category_id == category_id
        )

    if search and search.strip():

        search_text = (
            f"%{search.strip()}%"
        )

        query = query.filter(
            (
                TodoModel.title.ilike(
                    search_text
                )
            )
            |
            (
                TodoModel.description.ilike(
                    search_text
                )
            )
        )

    todos = (
        query
        .order_by(TodoModel.id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return todos

@app.get(
    "/todos/{todo_id}",
    response_model=TodoResponse
)
def get_todo(
    todo_id: int,
    db: Session = Depends(get_db)
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

@app.put(
    "/todos/{todo_id}",
    response_model=TodoResponse
)
def update_todo(
    todo_id: int,
    todo: TodoUpdate,
    db: Session = Depends(get_db)
):

    db_todo = (
        db.query(TodoModel)
        .filter(
            TodoModel.id == todo_id
        )
        .first()
    )

    if not db_todo:

        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    data = todo.model_dump(
        exclude_unset=True
    )

    if "category_id" in data:

        category = (
            db.query(CategoryModel)
            .filter(
                CategoryModel.id
                == data["category_id"]
            )
            .first()
        )

        if not category:

            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )

    if "title" in data:

        data["title"] = (
            data["title"].strip()
        )

    if "description" in data:

        data["description"] = (
            data["description"].strip()
        )

    for key, value in data.items():

        setattr(
            db_todo,
            key,
            value
        )

    db_todo.updated_at = current_time()

    db.commit()
    db.refresh(db_todo)

    return db_todo

@app.delete(
    "/todos/{todo_id}"
)
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db)
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

    db.delete(todo)
    db.commit()

    return {
        "message": "Todo deleted successfully",
        "deleted_todo_id": todo_id
    }

@app.get(
    "/todos/category/{category_id}",
    response_model=List[TodoResponse]
)
def get_todos_by_category(
    category_id: int,
    db: Session = Depends(get_db)
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

    return (
        db.query(TodoModel)
        .filter(
            TodoModel.category_id == category_id
        )
        .order_by(TodoModel.id)
        .all()
    )

@app.delete(
    "/todos/category/{category_id}"
)
def delete_todos_by_category(
    category_id: int,
    db: Session = Depends(get_db)
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

    deleted_count = (
        db.query(TodoModel)
        .filter(
            TodoModel.category_id == category_id
        )
        .delete(
            synchronize_session=False
        )
    )

    db.commit()

    return {
        "message": "Todos deleted successfully",
        "deleted_count": deleted_count
    }

