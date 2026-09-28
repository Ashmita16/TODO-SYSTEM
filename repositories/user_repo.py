from sqlalchemy.orm import Session
from models.user import User
from schemas.user_schema import UserCreate
from utils.auth import hash_password

class UserRepository:
    def get_by_username(self, db: Session, username: str):
        return db.query(User).filter(User.username == username).first()

    def create_user(self, db: Session, schema: UserCreate):
        db_user = User(
            username=schema.username,
            password_hash=hash_password(schema.password)
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def update_password(self, db: Session, user: User, new_password: str):
        user.password_hash = hash_password(new_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user