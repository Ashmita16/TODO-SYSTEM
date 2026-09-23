from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


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