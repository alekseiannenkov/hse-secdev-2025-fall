# syntax=docker/dockerfile:1.7

########################
# 1. Builder-образ
########################
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Обновляем pip и ставим зависимости в кэш wheels
RUN python -m pip install --upgrade pip

# Копируем только файлы зависимостей (для кеша слоёв)
# Если в репо другой файл зависимостей (pyproject/poetry) — поправишь здесь.
COPY requirements.txt .

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt


########################
# 2. Runtime-образ
########################
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_ENV=prod \
    PORT=8000

WORKDIR /app

# Создаём непривилегированного пользователя
RUN groupadd -r app && useradd -r -g app app

# Ставим зависимости из wheels
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

# Копируем приложение
COPY . /app

# Выдаём права пользователю app
RUN chown -R app:app /app

USER app

EXPOSE 8000

# HEALTHCHECK без curl, через стандартный модуль http.client
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import http.client, os, sys; \
port = int(os.getenv('PORT', '8000')); \
conn = http.client.HTTPConnection('127.0.0.1', port, timeout=2); \
try: \
    conn.request('GET', '/health'); \
    resp = conn.getresponse(); \
    sys.exit(0 if resp.status == 200 else 1); \
except Exception: \
    sys.exit(1)" || exit 1

# Стартуем uvicorn-приложение
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
