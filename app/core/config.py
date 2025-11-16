# app/core/config.py
import os

from pydantic import BaseModel, Field


class Settings(BaseModel):
    APP_NAME: str = "Wishlist"
    APP_ENV: str = Field(
        default=os.getenv("APP_ENV", "dev")
    )  # dev / test / prod / stage
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-insecure-key")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    DB_URL: str = os.getenv("DB_URL", "sqlite:///./wishlist.db")

    def __init__(self, **data):
        super().__init__(**data)
        if self.APP_ENV in {"prod", "stage"} and self.SECRET_KEY == "dev-insecure-key":
            raise ValueError(
                "Insecure SECRET_KEY is not allowed in APP_ENV=prod/stage. "
                "Set SECRET_KEY via environment."
            )


settings = Settings()
