"""Tests for /users endpoints."""


def test_get_users(client):
    resp = client.get("/users/")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert any(u["email"] == "jokotest123@email.com" for u in data)


def test_get_user_by_id(client):
    # find the seeded user's real id via the list endpoint
    users = client.get("/users/").get_json()
    joko = next(u for u in users if u["email"] == "jokotest123@email.com")

    resp = client.get(f"/users/{joko['id']}")
    assert resp.status_code == 200
    assert resp.get_json()["username"] == "Joko"


def test_get_user_not_found(client):
    resp = client.get("/users/9999")
    assert resp.status_code == 404


def test_create_user(client):
    resp = client.post("/users/", json={
        "username": "Alice",
        "email": "alice@example.com",
        "password": "secret123"
    })
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["status"] == "success"
    assert body["user"]["email"] == "alice@example.com"
    # password must never be returned
    assert "password" not in body["user"]
    assert "password_hash" not in body["user"]


def test_create_user_missing_fields(client):
    resp = client.post("/users/", json={"username": "NoEmail"})
    assert resp.status_code == 400


def test_create_user_invalid_email(client):
    resp = client.post("/users/", json={
        "username": "Bob",
        "email": "not-an-email",
        "password": "secret123"
    })
    assert resp.status_code == 400


def test_create_user_short_password(client):
    resp = client.post("/users/", json={
        "username": "Bob",
        "email": "bob@example.com",
        "password": "123"
    })
    assert resp.status_code == 400


def test_create_user_duplicate_email(client):
    client.post("/users/", json={
        "username": "Carol",
        "email": "carol@example.com",
        "password": "secret123"
    })
    resp = client.post("/users/", json={
        "username": "Carol2",
        "email": "carol@example.com",
        "password": "secret123"
    })
    assert resp.status_code == 409


def test_update_user(client):
    created = client.post("/users/", json={
        "username": "Dave",
        "email": "dave@example.com",
        "password": "secret123"
    }).get_json()
    uid = created["user"]["id"]

    resp = client.put(f"/users/{uid}", json={"username": "David"})
    assert resp.status_code == 200
    assert resp.get_json()["user"]["username"] == "David"


def test_update_user_not_found(client):
    resp = client.put("/users/9999", json={"username": "Ghost"})
    assert resp.status_code == 404


def test_delete_user(client):
    created = client.post("/users/", json={
        "username": "Eve",
        "email": "eve@example.com",
        "password": "secret123"
    }).get_json()
    uid = created["user"]["id"]

    resp = client.delete(f"/users/{uid}")
    assert resp.status_code == 200
    assert client.get(f"/users/{uid}").status_code == 404


def test_delete_user_not_found(client):
    resp = client.delete("/users/9999")
    assert resp.status_code == 404
