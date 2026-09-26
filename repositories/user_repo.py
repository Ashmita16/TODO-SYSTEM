from sqlalchemy.orm import Session
from models.user import User
from schemas.user_schemas import UserCreate
from utils.auth import hash_password

class UserRepository:
    def create_user(self, db: Session, schema: UserCreate) -> User:
        user = User(
            username=schema.username,
            hashed_password=hash_password(schema.password),
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def get_by_username(self, db: Session, username: str) -> User | None:
        return db.query(User).filter(User.username == username).first()

    def update_password(self, db: Session, user: User, new_password: str) -> User:
        user.hashed_password = hash_password(new_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user