from collections import defaultdict
import time
from typing import Dict, Tuple

from fastapi import HTTPException, Request, status

_attempts: Dict[str, Tuple[float, int]] = defaultdict(lambda: (0.0, 0))

WINDOW_SECONDS = 60
MAX_FAILED_ATTEMPTS = 5


def get_client_ip(request: Request) -> str:
    # В тестах это будет 127.0.0.1
    return request.client.host if request.client else "unknown"


def check_login_rate_limit(request: Request) -> str:
    """
    Проверяем, не превысил ли IP лимит неуспешных логинов.
    Если превысил — кидаем 429.
    Возвращаем ip, чтобы потом обновить счётчик.
    """
    ip = get_client_ip(request)
    now = time.time()

    start_ts, count = _attempts[ip]

    # Если окно истекло — начинаем новое
    if now - start_ts > WINDOW_SECONDS:
        start_ts, count = now, 0

    if count >= MAX_FAILED_ATTEMPTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many failed login attempts, please try again later",
        )

    _attempts[ip] = (start_ts, count)
    return ip


def register_failed_login(ip: str) -> None:
    now = time.time()
    start_ts, count = _attempts[ip]

    if now - start_ts > WINDOW_SECONDS:
        start_ts, count = now, 0

    _attempts[ip] = (start_ts, count + 1)


def reset_attempts(ip: str) -> None:
    _attempts.pop(ip, None)
