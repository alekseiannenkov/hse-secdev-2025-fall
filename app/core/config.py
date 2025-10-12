import os

from pydantic import BaseModel


class Settings(BaseModel):
    APP_NAME: str = "Wishlist"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-insecure-key")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    DB_URL: str = os.getenv("DB_URL", "sqlite:///./wishlist.db")


settings = Settings()
