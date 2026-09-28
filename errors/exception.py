from typing import Any


class AppError(Exception):
    code = "APP_ERROR"
    message = "An application error occurred"

    def __init__(self, detail: dict[str, Any]):
        self.detail = detail
        super().__init__(self.message)


class UserAlreadyExistsError(AppError):
    code = "USER_ALREADY_EXISTS"
    message = "User already exists"


class TodoAlreadyExistsError(AppError):
    code = "TODO_ALREADY_EXISTS"
    message = "Todo already exists"


class InvalidCredentialsError(AppError):
    code = "INVALID_CREDENTIALS"
    message = "Invalid credentials"


class AccountDisabledError(AppError):
    code = "ACCOUNT_DISABLED"
    message = "Account disabled"


class IncorrectPasswordError(AppError):
    code = "INCORRECT_PASSWORD"
    message = "Incorrect password"


class SamePasswordError(AppError):
    code = "SAME_PASSWORD"
    message = "Invalid new password"