from pydantic import BaseModel, EmailStr, Field

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

    class Config:
        from_attributes = True

class Token(BaseModel):
    message: str
    access_token: str
    token_type: str

class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(description="New password")