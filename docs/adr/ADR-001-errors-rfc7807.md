# ADR-001: Единый формат ошибок RFC 7807 с correlation_id
Дата: 2025-10-20
Статус: Accepted

## Context
API возвращал ошибки в произвольном формате и без идентификатора запроса, что усложняло диагностику и трассировку инцидентов.
Необходимо стандартизировать обработку ошибок и добавить correlation_id для связи логов.

## Decision
Внедрён стандарт [RFC 7807 (Problem Details for HTTP APIs)](https://datatracker.ietf.org/doc/html/rfc7807).
- Все ошибки сериализуются как `application/problem+json` с полями: `type`, `title`, `status`, `detail`, `correlation_id`.
- Middleware создаёт/прокидывает `X-Correlation-Id`.
- Поддерживаем коды 400 – 500.
- Метрика: 100 % ответов 4xx/5xx → корректный RFC 7807 JSON.

## Consequences
**Плюсы:** единообразие, улучшенная трассировка, совместимость с лог-агрегаторами.
**Минусы:** требуется обновление тестов и клиента.

## Links
- NFR-03 (ошибки RFC 7807), NFR-05 (трассировка)
- F1, R2 из Threat Model
- tests/test_errors_rfc7807.py::test_http_404_problem_json
- tests/test_errors_rfc7807.py::test_validation_error_problem_json
