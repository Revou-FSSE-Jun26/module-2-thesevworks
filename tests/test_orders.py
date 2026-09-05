"""Tests for /orders endpoints.

Orders are created by sending a list of items ({product_id, quantity}).
The server computes total_amount from real product prices — the client
never sends total_amount.
"""


def _seeded_user_id(client):
    users = client.get("/users/").get_json()
    return next(u for u in users if u["email"] == "jokotest123@email.com")["id"]


def _a_product(client):
    """Return the product with the most stock, so repeated order
    creation across tests doesn't run out."""
    products = client.get("/products/").get_json()
    return max(products, key=lambda p: p["stock"])


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


def test_create_order_total_calculated_by_system(client):
    user_id = _seeded_user_id(client)
    product = _a_product(client)
    quantity = 2

    resp = client.post("/orders/", json={
        "user_id": user_id,
        "items": [{"product_id": product["id"], "quantity": quantity}],
    })
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["status"] == "success"

    # server-computed total = product price * quantity
    expected_total = float(product["price"]) * quantity
    assert float(body["order"]["total_amount"]) == expected_total
    assert body["order"]["status"] == "pending"
    assert len(body["order"]["items"]) == 1


def test_create_order_ignores_client_total(client):
    """Even if the client sends total_amount, the server ignores it."""
    user_id = _seeded_user_id(client)
    product = _a_product(client)

    resp = client.post("/orders/", json={
        "user_id": user_id,
        "total_amount": 0.01,  # attempt to cheat
        "items": [{"product_id": product["id"], "quantity": 1}],
    })
    assert resp.status_code == 201
    # total reflects the real price, not the 0.01 the client sent
    assert float(resp.get_json()["order"]["total_amount"]) == float(product["price"])


def test_create_order_missing_items(client):
    user_id = _seeded_user_id(client)
    resp = client.post("/orders/", json={"user_id": user_id})
    assert resp.status_code == 400


def test_create_order_invalid_user(client):
    product = _a_product(client)
    resp = client.post("/orders/", json={
        "user_id": 9999,
        "items": [{"product_id": product["id"], "quantity": 1}],
    })
    assert resp.status_code == 400


def test_create_order_invalid_product(client):
    user_id = _seeded_user_id(client)
    resp = client.post("/orders/", json={
        "user_id": user_id,
        "items": [{"product_id": 9999, "quantity": 1}],
    })
    assert resp.status_code == 400


def test_create_order_zero_quantity(client):
    user_id = _seeded_user_id(client)
    product = _a_product(client)
    resp = client.post("/orders/", json={
        "user_id": user_id,
        "items": [{"product_id": product["id"], "quantity": 0}],
    })
    assert resp.status_code == 400
    assert "greater than 0" in resp.get_json()["error"]


def test_update_order_status(client):
    user_id = _seeded_user_id(client)
    product = _a_product(client)
    created = client.post("/orders/", json={
        "user_id": user_id,
        "items": [{"product_id": product["id"], "quantity": 1}],
    }).get_json()
    oid = created["order"]["id"]

    resp = client.put(f"/orders/{oid}", json={"status": "shipped"})
    assert resp.status_code == 200
    assert resp.get_json()["order"]["status"] == "shipped"


def test_update_order_rejects_total_amount(client):
    orders = client.get("/orders/").get_json()
    oid = orders[0]["id"]
    resp = client.put(f"/orders/{oid}", json={"total_amount": 999})
    assert resp.status_code == 400
    assert "calculated by the system" in resp.get_json()["error"]


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
    product = _a_product(client)
    created = client.post("/orders/", json={
        "user_id": user_id,
        "items": [{"product_id": product["id"], "quantity": 1}],
    }).get_json()
    oid = created["order"]["id"]

    resp = client.delete(f"/orders/{oid}")
    assert resp.status_code == 200
    assert client.get(f"/orders/{oid}").status_code == 404


def test_delete_order_not_found(client):
    resp = client.delete("/orders/9999")
    assert resp.status_code == 404
