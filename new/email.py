from pydantic_settings import BaseSettings, SettingsConfigDict


class EmailSettings(BaseSettings):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int = 465
    MAIL_SERVER: str = "sandbox.smtp.mailtrap.io"
    MAIL_FROM_NAME: str = "TODO MANAGEMENT SYSTEM"
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False

    model_config = SettingsConfigDict(
        env_file=".env.dev",
        env_file_encoding="utf-8",
        extra="ignore"
    )


email_settings = EmailSettings()