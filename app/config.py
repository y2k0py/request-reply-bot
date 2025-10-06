from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # Database
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "test_db"
    DB_USER: str = "postgres"
    DB_PASS: str = "testpass"

    DEBUG: bool = True

    TELEGRAM_ADMIN_ID: int
    SECRET_BOT_KEY: str = 'test-secret-change-for-prod-lrefjghieu3hfg39'

    # aiogram
    TELEGRAM_BOT_TOKEN: str


settings = Settings()