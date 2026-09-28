from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from dependencies.db_dependency import get_db
from dependencies.user_dependency import get_current_user
from schemas.user_schema import (
    UserCreate, 
    UserLogin, 
    UserResponse, 
    Token, 
    PasswordChange, 
    PasswordChangeResponse
)
from services.user_service import UserService
from models.user import User

router = APIRouter(prefix="/api/auth", tags=["Authentication"])
user_service = UserService()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(schema: UserCreate, db: Session = Depends(get_db)):
    return user_service.register_user(db, schema)

@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    access_token, issued_at = user_service.authenticate_user(db, credentials.username, credentials.password)
    return {
        "message": "LOGIN SUCCESSFUL",
        "access_token": access_token,
        "token_type": "bearer",
        "issued_at": issued_at
    }

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/change-password", response_model=PasswordChangeResponse, status_code=status.HTTP_200_OK)
def change_password(
    schema: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return user_service.change_password(db, current_user, schema)