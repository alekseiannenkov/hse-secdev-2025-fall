from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register_and_login():
    r = client.post(
        "/auth/register", json={"email": "u1@example.com", "password": "Password123"}
    )
    assert r.status_code == 201
    token = r.json()["access_token"]
    assert token

    r2 = client.post(
        "/auth/login", json={"email": "u1@example.com", "password": "Password123"}
    )
    assert r2.status_code == 200
    assert r2.json()["access_token"]
    # com
