from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DateTime
)
from sqlalchemy.orm import relationship

from db.database import Base


def kolkata_now():
    return datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).replace(tzinfo=None)


class Category(Base):
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
        nullable=True
    )

    todos = relationship(
        "Todo",
        back_populates="category"
    )


class Todo(Base):
    __tablename__ = "todos"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String,
        index=True,
        nullable=False
    )

    description = Column(
        String,
        nullable=True
    )

    is_completed = Column(
        Boolean,
        default=False,
        nullable=False
    )

    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=kolkata_now,
        nullable=False
    )

    updated_at = Column(
        DateTime,
        default=kolkata_now,
        onupdate=kolkata_now,
        nullable=False
    )

    category = relationship(
        "Category",
        back_populates="todos"
    )

    user = relationship(
        "User",
        back_populates="todos"
    )