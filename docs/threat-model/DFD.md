```mermaid
flowchart LR
    subgraph External["External App (Client / Browser / Mobile)"]
        U[Пользователь]
    end

    subgraph Edge["Trust Boundary: Edge (Uvicorn / FastAPI API Gateway)"]
        GW[API Gateway / FastAPI Router]
        AUTH[Auth Service]
        WISH[Wishes Service]
    end

    subgraph Core["Trust Boundary: Core (App Logic & Data Access)"]
        DB[(SQLite — wishlist.db)]
    end

    %% Потоки данных
    U -->|F1: HTTPS POST /auth/register| GW
    GW -->|F2: запрос регистрации → Auth Service| AUTH
    AUTH -->|F3: INSERT user (Argon2id hash)| DB

    U -->|F4: HTTPS POST /auth/login| GW
    GW -->|F5: проверка пароля + JWT| AUTH
    AUTH -->|F6: выдача access token| U

    U -->|F7: HTTPS GET/POST /wishes (JWT)| GW
    GW -->|F8: CRUD операции → Wishes Service| WISH
    WISH -->|F9: SELECT/UPDATE Wish| DB
