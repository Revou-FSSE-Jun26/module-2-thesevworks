"""Tests for /products endpoints."""


def test_get_products(client):
    resp = client.get("/products/")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) >= 2  # two seeded products


def test_get_product_by_id(client):
    # find the seeded product's real id via the list endpoint
    products = client.get("/products/").get_json()
    laptop = next(p for p in products if p["product_name"] == "Laptop")

    resp = client.get(f"/products/{laptop['id']}")
    assert resp.status_code == 200
    assert resp.get_json()["product_name"] == "Laptop"


def test_get_product_not_found(client):
    resp = client.get("/products/9999")
    assert resp.status_code == 404


def test_create_product(client, admin_headers):
    # use the seeded category id
    category = client.get("/category/").get_json()[0]

    resp = client.post("/products/", json={
        "category_id": category["id"],
        "product_name": "Mouse",
        "description": "Wireless mouse",
        "price": 25.5,
        "stock": 100
    }, headers=admin_headers)
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["status"] == "success"
    assert body["product"]["product_name"] == "Mouse"


def test_create_product_missing_fields(client, admin_headers):
    resp = client.post("/products/", json={"product_name": "Incomplete"}, headers=admin_headers)
    assert resp.status_code == 400
    assert "Missing required fields" in resp.get_json()["error"]


def test_create_product_negative_price(client, admin_headers):
    category = client.get("/category/").get_json()[0]
    resp = client.post("/products/", json={
        "category_id": category["id"],
        "product_name": "Bad",
        "price": -5,
        "stock": 10
    }, headers=admin_headers)
    assert resp.status_code == 400


def test_create_product_zero_price(client, admin_headers):
    category = client.get("/category/").get_json()[0]
    resp = client.post("/products/", json={
        "category_id": category["id"],
        "product_name": "ZeroPrice",
        "price": 0,
        "stock": 10
    }, headers=admin_headers)
    assert resp.status_code == 400
    assert "price must be greater than 0" in resp.get_json()["error"]


def test_create_product_negative_stock(client, admin_headers):
    category = client.get("/category/").get_json()[0]
    resp = client.post("/products/", json={
        "category_id": category["id"],
        "product_name": "NegStock",
        "price": 10,
        "stock": -1
    }, headers=admin_headers)
    assert resp.status_code == 400
    assert "stock cannot be negative" in resp.get_json()["error"]


def test_create_product_zero_stock_allowed(client, admin_headers):
    category = client.get("/category/").get_json()[0]
    resp = client.post("/products/", json={
        "category_id": category["id"],
        "product_name": "ZeroStock",
        "price": 10,
        "stock": 0
    }, headers=admin_headers)
    assert resp.status_code == 201


def test_create_product_invalid_price_type(client, admin_headers):
    category = client.get("/category/").get_json()[0]
    resp = client.post("/products/", json={
        "category_id": category["id"],
        "product_name": "Bad",
        "price": "abc",
        "stock": 10
    }, headers=admin_headers)
    assert resp.status_code == 400


def test_update_product(client, admin_headers):
    category = client.get("/category/").get_json()[0]
    created = client.post("/products/", json={
        "category_id": category["id"],
        "product_name": "Headset",
        "price": 45,
        "stock": 20
    }, headers=admin_headers).get_json()
    pid = created["product"]["id"]

    resp = client.put(f"/products/{pid}", json={"price": 39.99, "stock": 15}, headers=admin_headers)
    assert resp.status_code == 200
    body = resp.get_json()
    assert float(body["product"]["price"]) == 39.99
    assert body["product"]["stock"] == 15


def test_update_product_not_found(client, admin_headers):
    resp = client.put("/products/9999", json={"price": 10}, headers=admin_headers)
    assert resp.status_code == 404


def test_update_product_invalid_category(client, admin_headers):
    products = client.get("/products/").get_json()
    pid = products[0]["id"]
    resp = client.put(f"/products/{pid}", json={"category_id": 9999}, headers=admin_headers)
    assert resp.status_code == 404


def test_delete_product(client, admin_headers):
    category = client.get("/category/").get_json()[0]
    created = client.post("/products/", json={
        "category_id": category["id"],
        "product_name": "Disposable",
        "price": 1,
        "stock": 1
    }, headers=admin_headers).get_json()
    pid = created["product"]["id"]

    resp = client.delete(f"/products/{pid}", headers=admin_headers)
    assert resp.status_code == 200
    assert client.get(f"/products/{pid}").status_code == 404


def test_delete_product_not_found(client, admin_headers):
    resp = client.delete("/products/9999", headers=admin_headers)
    assert resp.status_code == 404
