from contextlib import asynccontextmanager
from typing import Any, Dict
import uuid

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.db import init_db
from app.routers import auth, items, wishes

# --- Создание БД при импорте (нужно для pytest, чтобы таблицы существовали) ---
init_db()


def _problem_json(
    type_: str,
    title: str,
    status: int,
    detail: str | None,
    correlation_id: str,
) -> Dict[str, Any]:
    """RFC 7807 payload."""
    return {
        "type": type_,
        "title": title,
        "status": status,
        "detail": detail,
        "correlation_id": correlation_id,
    }


def _code_for_status(status_code: int) -> str:
    """Сопоставление HTTP-кодов со старыми короткими кодами (для legacy-совместимости)."""
    mapping = {
        400: "bad_request",
        401: "unauthorized",
        403: "forbidden",
        404: "not_found",
        409: "conflict",
        415: "unsupported_media_type",
        422: "validation_error",
        429: "too_many_requests",
        500: "internal_error",
    }
    return mapping.get(status_code, "error")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # безопасная инициализация БД при запуске приложения
    init_db()
    yield


app = FastAPI(title="Wishlist", lifespan=lifespan)


# --- Middleware: добавление correlation_id ---
@app.middleware("http")
async def add_correlation_id(request: Request, call_next):
    """Создаёт или прокидывает X-Correlation-Id для трассировки."""
    corr = request.headers.get("x-correlation-id") or str(uuid.uuid4())
    request.state.correlation_id = corr
    response = await call_next(request)
    response.headers["X-Correlation-Id"] = corr
    return response


# --- Регистрация роутеров ---
# ВАЖНО: без "/api", чтобы соответствовать тестам (/auth, /items, /wishes)
app.include_router(auth.router)
app.include_router(items.router)
app.include_router(wishes.router)


# --- Обработчики ошибок (RFC 7807 + legacy "error" для старых тестов) ---
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    corr = getattr(request.state, "correlation_id", None) or "unknown"
    short = _code_for_status(exc.status_code)
    title = short.replace("_", " ")
    payload = _problem_json(
        type_=f"about:blank#{short}",
        title=title,
        status=exc.status_code,
        detail=str(exc.detail),
        correlation_id=corr,
    )
    # legacy-обёртка под старые тесты
    legacy = {
        "error": {"code": short, "message": str(exc.detail) if exc.detail else title}
    }
    payload.update(legacy)
    return JSONResponse(
        payload, status_code=exc.status_code, media_type="application/problem+json"
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    corr = getattr(request.state, "correlation_id", None) or "unknown"
    short = "validation_error"
    payload = _problem_json(
        type_=f"about:blank#{short}",
        title="validation error",
        status=422,
        detail=str(exc.errors()),
        correlation_id=corr,
    )
    # legacy-обёртка под старые тесты
    legacy = {"error": {"code": short, "message": "validation error"}}
    payload.update(legacy)
    return JSONResponse(payload, status_code=422, media_type="application/problem+json")


# --- Health и корень ---
@app.get("/")
def root():
    return {"status": "ok", "app": "Wishlist"}


@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok"}
