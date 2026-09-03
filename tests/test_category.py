"""Tests for /category endpoints."""


def test_get_categories(client):
    resp = client.get("/category/")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert any(c["category_name"] == "Electronics" for c in data)


def test_get_category_by_id(client):
    # id 1 is the seeded Electronics category
    resp = client.get("/category/1")
    assert resp.status_code == 200
    assert resp.get_json()["category_name"] == "Electronics"


def test_get_category_not_found(client):
    resp = client.get("/category/9999")
    assert resp.status_code == 404


def test_create_category(client):
    resp = client.post("/category/", json={
        "category_name": "Books",
        "description": "All kinds of books"
    })
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["status"] == "success"
    assert body["category"]["category_name"] == "Books"


def test_create_category_missing_name(client):
    resp = client.post("/category/", json={"description": "no name"})
    assert resp.status_code == 400
    assert "category_name" in resp.get_json()["error"]


def test_create_category_no_body(client):
    resp = client.post("/category/", data="not json", content_type="text/plain")
    assert resp.status_code == 400


def test_create_category_duplicate(client):
    client.post("/category/", json={"category_name": "Toys"})
    resp = client.post("/category/", json={"category_name": "Toys"})
    assert resp.status_code == 409


def test_update_category(client):
    created = client.post("/category/", json={"category_name": "Garden"}).get_json()
    cat_id = created["category"]["id"]

    resp = client.put(f"/category/{cat_id}", json={"description": "Garden tools"})
    assert resp.status_code == 200
    assert resp.get_json()["category"]["description"] == "Garden tools"


def test_update_category_not_found(client):
    resp = client.put("/category/9999", json={"category_name": "X"})
    assert resp.status_code == 404


def test_delete_category(client):
    created = client.post("/category/", json={"category_name": "Temporary"}).get_json()
    cat_id = created["category"]["id"]

    resp = client.delete(f"/category/{cat_id}")
    assert resp.status_code == 200

    # confirm it's gone
    assert client.get(f"/category/{cat_id}").status_code == 404


def test_delete_category_not_found(client):
    resp = client.delete("/category/9999")
    assert resp.status_code == 404
