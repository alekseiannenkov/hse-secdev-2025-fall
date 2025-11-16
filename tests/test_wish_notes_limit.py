from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def auth_token(email="notes@example.com", password="Password123"):
    client.post("/auth/register", json={"email": email, "password": password})
    return client.post(
        "/auth/login", json={"email": email, "password": password}
    ).json()["access_token"]


def test_cannot_create_wish_with_too_long_notes():
    token = auth_token()
    headers = {"Authorization": f"Bearer {token}"}

    too_long_notes = "x" * 2001

    r = client.post(
        "/wishes/",
        headers=headers,
        json={"title": "Big note", "notes": too_long_notes},
    )

    assert r.status_code == 422
