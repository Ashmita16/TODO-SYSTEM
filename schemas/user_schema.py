from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_serializer
)


class UserLogin(BaseModel):
    username: EmailStr
    password: str


class UserCreate(BaseModel):
    username: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: EmailStr
    is_active: bool
    password_changed_at: Optional[datetime] = None

    @field_serializer("password_changed_at")
    def serialize_dt(
        self,
        dt: Optional[datetime],
        _info
    ):
        if dt is not None:
            return dt.strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        return None

    class Config:
        from_attributes = True


class Token(BaseModel):
    message: str
    access_token: str
    token_type: str
    issued_at: str


class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(
        description="New password"
    )


class PasswordChangeResponse(BaseModel):
    message: str
    password_changed_at: str