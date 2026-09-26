from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.user_repo import UserRepository
from schemas.user_schemas import UserCreate, PasswordChange
from utils.auth import verify_password, create_access_token
from models.user import User

class UserService:
    def __init__(self):
        self.user_repo = UserRepository()

    def register_user(self, db: Session, schema: UserCreate):
        if self.user_repo.get_by_username(db, schema.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="ACCOUNT WITH THIS EMAIL ALREADY EXISTS!"
            )
        return self.user_repo.create_user(db, schema)

    def authenticate_user(self, db: Session, username: str, password: str) -> str:
        user = self.user_repo.get_by_username(db, username)
        
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="INVALID USERNAME OR PASSWORD!"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="USER ACCOUNT DISABLED!"
            )

        return create_access_token(data={"sub": user.username})

    def change_password(self, db: Session, current_user: User, schema: PasswordChange):
        if not verify_password(schema.current_password, current_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="INCORRECT CURRENT PASSWORD!"
            )
        
        if verify_password(schema.new_password, current_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="NEW PASSWORD CANNOT BE SAME AS CURRENT PASSWORD!"
            )

        self.user_repo.update_password(db, current_user, schema.new_password)
        return {"MESSAGE": "PASSWORD CHANGED SUCCESSFULLY!"}