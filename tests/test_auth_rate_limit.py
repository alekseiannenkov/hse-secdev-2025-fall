from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_rate_limit_on_failed_logins():
    client.post(
        "/auth/register",
        json={"email": "rate@example.com", "password": "Password123"},
    )

    for _ in range(5):
        r = client.post(
            "/auth/login",
            json={"email": "rate@example.com", "password": "WrongPassword"},
        )
        assert r.status_code == 401

    r = client.post(
        "/auth/login",
        json={"email": "rate@example.com", "password": "WrongPassword"},
    )
    assert r.status_code == 429
