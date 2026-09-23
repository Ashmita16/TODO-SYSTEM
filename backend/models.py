from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum as SQLEnum,
    Float,
    ForeignKey,
    Integer,
    String
)
from sqlalchemy.orm import relationship

from .database import Base


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

    id = Column(Integer, primary_key=True, index=True)

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
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    todos = relationship(
        "TodoModel",
        back_populates="category",
        cascade="all, delete-orphan"
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
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    category = relationship(
        "CategoryModel",
        back_populates="todos"
    )