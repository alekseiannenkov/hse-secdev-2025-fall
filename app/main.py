from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.db import init_db
from app.routers import auth, items, wishes

# --- Создание БД при импорте (нужно для pytest, чтобы таблицы существовали) ---
init_db()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Повторный вызов init_db() безопасен: создаёт таблицы, если их нет
    init_db()
    yield


app = FastAPI(title="Wishlist", lifespan=lifespan)


# --- Подключение роутеров ---
app.include_router(auth.router)
app.include_router(wishes.router)
app.include_router(items.router)


# --- Метаданные / здоровье ---
@app.get("/")
def root():
    return {"status": "ok", "app": "Wishlist"}


@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok"}


# --- Единый формат ошибок (для тестов и API) ---
def _code_for_status(status_code: int) -> str:
    """Возвращает код ошибки в нашем формате."""
    return {
        400: "bad_request",
        401: "unauthorized",
        403: "forbidden",
        404: "not_found",
        409: "conflict",
        422: "validation_error",
        500: "internal_error",
    }.get(status_code, "http_error")


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Все стандартные HTTP-ошибки → {"error": {...}}"""
    if isinstance(exc.detail, dict) and "error" in exc.detail:
        payload = exc.detail
    else:
        payload = {
            "error": {
                "code": _code_for_status(exc.status_code),
                "message": str(exc.detail),
            }
        }
    return JSONResponse(payload, status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Ошибки валидации схем FastAPI / Pydantic."""
    payload = {"error": {"code": "validation_error", "details": exc.errors()}}
    return JSONResponse(payload, status_code=422)
