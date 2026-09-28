from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Session

from repositories.user_repo import UserRepository
from schemas.user_schema import UserCreate, PasswordChange
from utils.auth import verify_password, create_access_token
from models.user import User

from errors.exception import (
    UserAlreadyExistsError,
    InvalidCredentialsError,
    AccountDisabledError,
    IncorrectPasswordError,
    SamePasswordError
)


class UserService:

    def __init__(self):
        self.user_repo = UserRepository()

    def register_user(
        self,
        db: Session,
        schema: UserCreate
    ):

        if self.user_repo.get_by_username(db, schema.username):

            raise UserAlreadyExistsError(
                detail={
                    "message": "Email with this user id already exists"
                }
            )

        return self.user_repo.create_user(
            db,
            schema
        )

    def authenticate_user(
        self,
        db: Session,
        username: str,
        password: str
    ):

        user = self.user_repo.get_by_username(
            db,
            username
        )

        if not user or not verify_password(
            password,
            user.password_hash
        ):

            raise InvalidCredentialsError(
                detail={
                    "message": "Invalid username or password"
                }
            )

        if not user.is_active:

            raise AccountDisabledError(
                detail={
                    "message": "User account is disabled"
                }
            )

        return create_access_token(
            data={
                "sub": user.username
            }
        )

    def change_password(
        self,
        db: Session,
        current_user: User,
        schema: PasswordChange
    ):

        if not verify_password(
            schema.current_password,
            current_user.password_hash
        ):

            raise IncorrectPasswordError(
                detail={
                    "message": "The current password is incorrect"
                }
            )

        if verify_password(
            schema.new_password,
            current_user.password_hash
        ):

            raise SamePasswordError(
                detail={
                    "message": "New password cannot be same as current password"
                }
            )

        now_utc = datetime.now(timezone.utc)

        current_user.password_changed_at = now_utc

        self.user_repo.update_password(
            db,
            current_user,
            schema.new_password
        )

        ist_time = now_utc.astimezone(
            ZoneInfo("Asia/Kolkata")
        )

        return {
            "message": "PASSWORD CHANGED SUCCESSFULLY!",
            "password_changed_at": ist_time.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }