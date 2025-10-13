from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def auth_token(email="owner@example.com", password="Password123"):
    client.post("/auth/register", json={"email": email, "password": password})
    return client.post(
        "/auth/login", json={"email": email, "password": password}
    ).json()["access_token"]


def test_crud_and_filter_and_ownership():
    t_owner = auth_token()
    h_owner = {"Authorization": f"Bearer {t_owner}"}

    # create
    w = {"title": "Steam Deck", "price_estimate": 499.99}
    r = client.post("/wishes/", headers=h_owner, json=w)
    assert r.status_code == 201
    wid = r.json()["id"]

    # list
    r = client.get("/wishes", headers=h_owner)
    assert r.status_code == 200
    assert any(x["id"] == wid for x in r.json())

    # filter price<
    r = client.get("/wishes", headers=h_owner, params={"price<": 500})
    assert r.status_code == 200
    assert any(x["id"] == wid for x in r.json())

    r = client.get("/wishes", headers=h_owner, params={"price<": 400})
    assert r.status_code == 200
    assert not any(x["id"] == wid for x in r.json())

    # ownership
    t_other = auth_token("other@example.com", "Password123")
    h_other = {"Authorization": f"Bearer {t_other}"}

    r = client.get(f"/wishes/{wid}", headers=h_other)
    assert r.status_code == 403

    # update/delete by owner
    r = client.put(f"/wishes/{wid}", headers=h_owner, json={"title": "Steam Deck OLED"})
    assert r.status_code == 200 and r.json()["title"] == "Steam Deck OLED"

    r = client.delete(f"/wishes/{wid}", headers=h_owner)
    assert r.status_code == 204
