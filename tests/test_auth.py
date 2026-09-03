"""Tests for /auth endpoints."""


def test_login_success(client):
    # create a user first
    client.post("/users/", json={
        "username": "LoginUser",
        "email": "login@example.com",
        "password": "secret123"
    })

    resp = client.post("/auth/login", json={
        "email": "login@example.com",
        "password": "secret123"
    })
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["success"] is True
    assert "token" in body


def test_login_wrong_password(client):
    client.post("/users/", json={
        "username": "WrongPass",
        "email": "wrongpass@example.com",
        "password": "secret123"
    })

    resp = client.post("/auth/login", json={
        "email": "wrongpass@example.com",
        "password": "incorrect"
    })
    assert resp.status_code == 401
    assert resp.get_json()["success"] is False


def test_login_unknown_email(client):
    resp = client.post("/auth/login", json={
        "email": "nobody@example.com",
        "password": "secret123"
    })
    assert resp.status_code == 401


def test_login_missing_fields(client):
    resp = client.post("/auth/login", json={"email": "x@example.com"})
    assert resp.status_code == 400


def test_login_no_body(client):
    resp = client.post("/auth/login", data="x", content_type="text/plain")
    assert resp.status_code == 400
