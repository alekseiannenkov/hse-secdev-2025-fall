| RiskID | Описание | Связь (F/NFR) | L | I | Risk | Стратегия | Владелец | Срок | Критерий закрытия |
|--------|-----------|---------------|---|---|------|-----------|-----------|------|-------------------|
| R1 | Подмена email при регистрации | F1, NFR-01 | 2 | 3 | 6 | Снизить | @alekseiannenkov | текущий релиз | pytest unique email |
| R2 | Брутфорс логина | F4, NFR-09 | 4 | 4 | 16 | Снизить | @alekseiannenkov | следующий релиз | middleware rate-limit |
| R3 | Подмена hash | F5, NFR-01 | 1 | 4 | 4 | Избежать | @alekseiannenkov | постоянно | passlib argon2id config |
| R4 | Кража JWT токена | F6, NFR-02 | 2 | 5 | 10 | Снизить | @alekseiannenkov | текущий релиз | exp ≤ 24h |
| R5 | Доступ к чужим wishes | F7, NFR-03 | 3 | 5 | 15 | Снизить | @alekseiannenkov | текущий релиз | pytest CRUD ownership |
| R6 | Утечка деталей ошибок | F8, NFR-05 | 2 | 4 | 8 | Снизить | @alekseiannenkov | текущий релиз | pytest test_errors |
| R7 | SQL-инъекция | F9, NFR-05 | 1 | 5 | 5 | Избежать | @alekseiannenkov | постоянно | ORM защитен |
| R8 | Отказ при нагрузке | Core, NFR-10 | 3 | 3 | 9 | Снизить | @alekseiannenkov | следующий релиз | локальный ops тест |
| R9 | Коммит секретов в репо | Repo, NFR-07 | 2 | 4 | 8 | Избежать | @alekseiannenkov | постоянно | pre-commit + .env |
| R10 | Уязвимости зависимостей | Project, NFR-08 | 3 | 3 | 9 | Снизить | @alekseiannenkov | итеративно | GitHub Security Issues |
