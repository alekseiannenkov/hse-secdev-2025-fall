# Non-Functional Requirements — Wishlist

ID | Название | Описание | Метрика/Порог | Проверка (чем/где) | Компонент | Приоритет
---|----------|----------|---------------|---------------------|-----------|----------
NFR-01 | Хеш паролей (Argon2id) | Пароли храним только в виде Argon2id-хеша с устойчивыми параметрами | time_cost ≥ 2; memory_cost ≥ 64 MiB; parallelism ≥ 2 | unit-тест параметров passlib; код-ревью | Auth | must
NFR-02 | TTL JWT | Время жизни access-токена ограничено | exp ≤ 24h | интеграционный тест: токен с истёкшим exp → 401 | Auth | must
NFR-03 | Владелец-only | Пользователь имеет доступ только к своим wishes | 100% запросов к чужим ресурсам → 403 | pytest (ownership в CRUD) | Wishes | must
NFR-04 | Валидация цены | `price_estimate` неотрицательная | все значения ≥ 0; пустое допускается | pydantic-schema тесты; ручные сценарии | Wishes | high
NFR-05 | Контракт ошибок | Единый JSON-формат ошибок | 100% HTTP/422 → `{"error":{...}}` | pytest (`tests/test_errors.py`) | API | high
NFR-06 | Фильтр по цене | Фильтрация по `price<` корректна | Для набора данных: выборка < порога | интеграционный тест `/wishes?price%3C=...` | Wishes | medium
NFR-07 | Отсутствие секретов в Git | Секреты не коммитятся | 0 утечек | pre-commit / ревью; `.env` в `.gitignore` | Repo | must
NFR-08 | SLA на устранение уязвимостей | High/Critical исправляются быстро | High ≤ 7 дней; Critical ≤ 3 дней | Security Issues + Milestones | Проект | high
NFR-09 | Rate limiting (auth) | Защита от брутфорса на /auth | ≥ 60 req/min/IP → 429 | план: middleware/edge; тест сценариев | Edge/API | medium
NFR-10 | Доступность и ошибки | Доля 5xx низкая при ручной нагрузке | 5xx < 1% при p95 < 200мс (локально) | упрощённый нагрузочный прогон (позже) | API | medium

**Заметки:**
- NFR-09/10 — помечены как medium и могут быть реализованы позже (создаём задачи в backlog).
- Для NFR-01 конкретные параметры задаются в конфиге passlib (argon2id).
