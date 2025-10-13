| Поток / Элемент | Угроза (STRIDE) | Риск | Контроль | Ссылка на NFR | Проверка / Артефакт |
|-----------------|------------------|------|-----------|---------------|---------------------|
| F1 /auth/register | S: Spoofing (регистрация под чужим email) | R1 | Проверка уникальности email | NFR-01 | pytest test_auth |
| F4 /auth/login | D: Брутфорс | R2 | Rate limit на /auth (60 req/min/IP) | NFR-09 | edge middleware |
| F5 /auth/login | T: Tampering (подмена hash) | R3 | Argon2id, salt, проверка hash | NFR-01 | unit test passlib |
| F6 выдача JWT | S/I: Кража токена | R4 | TTL ≤ 24h, подпись JWT | NFR-02 | pytest exp validation |
| F7 /wishes | E: Elevation of Privilege (чтение чужих данных) | R5 | Проверка owner_id | NFR-03 | pytest CRUD ownership |
| F8 внутренний вызов | I: Information Disclosure (детали ошибок) | R6 | Единый JSON формат ошибок | NFR-05 | pytest test_errors |
| F9 работа с БД | T: SQL-инъекция | R7 | ORM SQLAlchemy | NFR-05 | код-ревью |
| Core / Database | D: DoS при высокой нагрузке | R8 | Нагрузочное тестирование | NFR-10 | ops benchmark |
