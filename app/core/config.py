import os

from pydantic import BaseModel, Field


class Settings(BaseModel):
    APP_NAME: str = "Wishlist"
    APP_ENV: str = Field(
        default=os.getenv("APP_ENV", "dev")
    )  # dev / test / prod / stage
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-insecure-key")
    DB_URL: str = os.getenv("DB_URL", "sqlite:///./wishlist.db")

    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", str(60 * 24))
    )

    HTTP_CONNECT_TIMEOUT: float = float(os.getenv("HTTP_CONNECT_TIMEOUT", "2.0"))
    HTTP_READ_TIMEOUT: float = float(os.getenv("HTTP_READ_TIMEOUT", "5.0"))
    HTTP_TOTAL_TIMEOUT: float = float(os.getenv("HTTP_TOTAL_TIMEOUT", "6.0"))
    HTTP_MAX_RETRIES: int = int(os.getenv("HTTP_MAX_RETRIES", "3"))

    def __init__(self, **data):
        super().__init__(**data)
        # P06: защитный контроль для секретного ключа
        if self.APP_ENV in {"prod", "stage"} and self.SECRET_KEY == "dev-insecure-key":
            raise ValueError(
                "Insecure SECRET_KEY is not allowed in APP_ENV=prod/stage. "
                "Set SECRET_KEY via environment."
            )


settings = Settings()
