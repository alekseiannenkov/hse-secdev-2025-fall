import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings


class Base(DeclarativeBase):
    pass


connect_args = (
    {"check_same_thread": False} if settings.DB_URL.startswith("sqlite") else {}
)

engine = create_engine(
    settings.DB_URL,
    echo=False,
    future=True,
    connect_args=connect_args,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def init_db():
    """
    Гарантированно поднимает (и при необходимости пересоздаёт) схему БД.

    Особенность: при запуске под pytest переменная окружения PYTEST_CURRENT_TEST
    автоматически установлена. В этом случае мы сначала делаем drop_all(), чтобы
    прогон тестов всегда начинался с чистой базы и не ловил 409/state leakage.
    """
    from app.models.user import User  # noqa
    from app.models.wish import Wish  # noqa

    is_pytest = bool(os.getenv("PYTEST_CURRENT_TEST"))

    if is_pytest:
        Base.metadata.drop_all(bind=engine)

    Base.metadata.create_all(bind=engine)
