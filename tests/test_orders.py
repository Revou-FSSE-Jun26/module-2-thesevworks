"""Tests for /orders endpoints."""


def _seeded_user_id(client):
    users = client.get("/users/").get_json()
    return next(u for u in users if u["email"] == "jokotest123@email.com")["id"]


def test_get_orders(client):
    resp = client.get("/orders/")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) >= 1  # one seeded order


def test_get_order_by_id(client):
    orders = client.get("/orders/").get_json()
    oid = orders[0]["id"]

    resp = client.get(f"/orders/{oid}")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "pending"


def test_get_order_not_found(client):
    resp = client.get("/orders/9999")
    assert resp.status_code == 404


def test_create_order(client):
    user_id = _seeded_user_id(client)
    resp = client.post("/orders/", json={
        "user_id": user_id,
        "total_amount": 150.75,
        "status": "pending"
    })
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["status"] == "success"
    assert body["order"]["status"] == "pending"


def test_create_order_missing_fields(client):
    user_id = _seeded_user_id(client)
    resp = client.post("/orders/", json={"user_id": user_id})
    assert resp.status_code == 400


def test_create_order_invalid_user(client):
    resp = client.post("/orders/", json={
        "user_id": 9999,
        "total_amount": 10,
        "status": "pending"
    })
    assert resp.status_code == 400


def test_create_order_negative_total(client):
    user_id = _seeded_user_id(client)
    resp = client.post("/orders/", json={
        "user_id": user_id,
        "total_amount": -10,
        "status": "pending"
    })
    assert resp.status_code == 400


def test_update_order_status(client):
    user_id = _seeded_user_id(client)
    created = client.post("/orders/", json={
        "user_id": user_id,
        "total_amount": 50,
        "status": "pending"
    }).get_json()
    oid = created["order"]["id"]

    resp = client.put(f"/orders/{oid}", json={"status": "shipped"})
    assert resp.status_code == 200
    assert resp.get_json()["order"]["status"] == "shipped"


def test_update_order_invalid_status(client):
    orders = client.get("/orders/").get_json()
    oid = orders[0]["id"]
    resp = client.put(f"/orders/{oid}", json={"status": "flying"})
    assert resp.status_code == 400


def test_update_order_not_found(client):
    resp = client.put("/orders/9999", json={"status": "shipped"})
    assert resp.status_code == 404


def test_delete_order(client):
    user_id = _seeded_user_id(client)
    created = client.post("/orders/", json={
        "user_id": user_id,
        "total_amount": 20,
        "status": "pending"
    }).get_json()
    oid = created["order"]["id"]

    resp = client.delete(f"/orders/{oid}")
    assert resp.status_code == 200
    assert client.get(f"/orders/{oid}").status_code == 404


def test_delete_order_not_found(client):
    resp = client.delete("/orders/9999")
    assert resp.status_code == 404
