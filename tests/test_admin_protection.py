"""Bug-condition exploration test — Property 1: Admin Access Enforcement.

Spec: admin-role-protection (bugfix).
Requirements covered: 1.1, 1.2, 1.3, 1.4, 1.5, 2.1, 2.2, 2.4, 2.5.

This test encodes the EXPECTED (correct/secure) behavior described by Property 1
(Fix Checking) in the bugfix design:

    FOR ALL req WHERE isBugCondition(req) DO
        result <- F'(req)
        ASSERT result.status IN {401, 403}
           AND no_side_effect(result)
    END FOR

A request is a bug condition when it reaches a protected admin endpoint without a
valid admin JWT:
    (/users   with GET/PUT/DELETE) OR
    (/products with POST/PUT/DELETE) OR
    (/category with POST/PUT/DELETE)
carried WITHOUT a valid admin identity.

IMPORTANT (exploration test, pre-fix): on the CURRENT unfixed code the admin guards
are commented out, so these protected endpoints are reachable by anyone. Therefore
this test is EXPECTED TO FAIL on the unfixed code — the failure is the counterexample
that PROVES the bug exists. Do NOT weaken these assertions to make them pass; the fix
tasks (3.x) will make the code satisfy this test.
"""

import pytest

from app import db as _db
from models import Product, Category, User


# --- helpers -----------------------------------------------------------------

def _seed_buyer_and_login(client):
    """Return a REAL buyer JWT by registering a buyer and logging in.

    Registration (POST /users/) is public and always creates a 'buyer'. We log in
    through POST /auth/login so the token carries the real claims {email, role=buyer}
    with identity=str(user.id) — exactly what the app issues in production.
    """
    client.post("/users/", json={
        "username": "BuyerForAdminTest",
        "email": "buyer_admin_test@example.com",
        "password": "secret123",
    })
    resp = client.post("/auth/login", json={
        "email": "buyer_admin_test@example.com",
        "password": "secret123",
    })
    assert resp.status_code == 200, "login harness precondition failed"
    return resp.get_json()["token"]


def _bearer(token):
    return {"Authorization": f"Bearer {token}"}


# --- Property 1: Bug Condition - Admin Access Enforcement --------------------

def test_delete_users_without_jwt_is_rejected_and_no_side_effect(app, client):
    """DELETE /users/<id> without Authorization must be rejected (401) and must
    NOT delete the user.

    Requirements: 1.2, 2.2 (and 1.1). Expected: 401. Current unfixed code: 200 + deletes.
    """
    # Arrange: a user that exists and must survive the rejected request.
    created = client.post("/users/", json={
        "username": "Victim",
        "email": "victim_delete@example.com",
        "password": "secret123",
    }).get_json()
    uid = created["user"]["id"]

    # Act: no Authorization header -> this is a bug-condition request.
    resp = client.delete(f"/users/{uid}")

    # Assert: refused ...
    assert resp.status_code in (401, 403), (
        f"COUNTEREXAMPLE: DELETE /users/{uid} without Authorization returned "
        f"{resp.status_code} (expected 401/403); protected endpoint is unguarded."
    )
    # ... and no side effect: the user still exists in the database.
    with app.app_context():
        assert _db.session.get(User, uid) is not None, (
            f"SIDE EFFECT COUNTEREXAMPLE: user {uid} was deleted by an unauthenticated "
            f"DELETE /users/{uid} request."
        )


def test_get_users_without_jwt_is_rejected(client):
    """GET /users/ without Authorization must be rejected (does not leak user data).

    Requirements: 1.1, 2.1. Expected: 401. Current unfixed code: 200 + returns users.
    """
    resp = client.get("/users/")
    assert resp.status_code in (401, 403), (
        f"COUNTEREXAMPLE: GET /users/ without Authorization returned {resp.status_code} "
        f"(expected 401/403); user list is readable without an admin JWT."
    )


def test_post_products_without_jwt_is_rejected_and_no_side_effect(app, client):
    """POST /products/ without Authorization must be rejected (401) and must NOT
    create a product.

    Requirements: 1.4, 2.4. Expected: 401. Current unfixed code: 201 + creates.
    """
    # Need a valid category id to form an otherwise-valid create payload.
    with app.app_context():
        category = Category.query.first()
        assert category is not None, "seed precondition: at least one category"
        category_id = category.id
        before = Product.query.count()

    resp = client.post("/products/", json={
        "category_id": category_id,
        "product_name": "UnauthorizedProduct",
        "price": 10.0,
        "stock": 5,
    })

    assert resp.status_code in (401, 403), (
        f"COUNTEREXAMPLE: POST /products/ without Authorization returned "
        f"{resp.status_code} (expected 401/403); product creation is unguarded."
    )
    with app.app_context():
        after = Product.query.count()
        assert after == before, (
            f"SIDE EFFECT COUNTEREXAMPLE: an unauthenticated POST /products/ created a "
            f"product (count {before} -> {after})."
        )


def test_put_category_without_jwt_is_rejected_and_no_side_effect(app, client):
    """PUT /category/<id> without Authorization must be rejected (401) and must NOT
    modify the category.

    Requirements: 1.5, 2.5. Expected: 401. Current unfixed code: 200 + updates.
    """
    with app.app_context():
        category = Category.query.first()
        assert category is not None, "seed precondition: at least one category"
        cid = category.id
        original_name = category.category_name

    resp = client.put(f"/category/{cid}", json={"category_name": "HackedName"})

    assert resp.status_code in (401, 403), (
        f"COUNTEREXAMPLE: PUT /category/{cid} without Authorization returned "
        f"{resp.status_code} (expected 401/403); category update is unguarded."
    )
    with app.app_context():
        current = _db.session.get(Category, cid)
        assert current is not None and current.category_name == original_name, (
            f"SIDE EFFECT COUNTEREXAMPLE: an unauthenticated PUT /category/{cid} changed "
            f"the category name from {original_name!r} to {current.category_name!r}."
        )


def test_delete_products_with_buyer_jwt_is_forbidden_and_no_side_effect(app, client):
    """Edge case (non-admin identity): DELETE /products/<id> with a REAL buyer JWT
    must be rejected (403) and must NOT delete the product.

    Requirements: 1.4, 2.4. Expected: 403 (valid token, wrong role).
    Current unfixed code: 200 + deletes.
    """
    token = _seed_buyer_and_login(client)

    with app.app_context():
        product = Product.query.first()
        assert product is not None, "seed precondition: at least one product"
        pid = product.id

    resp = client.delete(f"/products/{pid}", headers=_bearer(token))

    assert resp.status_code in (401, 403), (
        f"COUNTEREXAMPLE: DELETE /products/{pid} with a buyer JWT returned "
        f"{resp.status_code} (expected 403); non-admin role can mutate products."
    )
    with app.app_context():
        assert _db.session.get(Product, pid) is not None, (
            f"SIDE EFFECT COUNTEREXAMPLE: a buyer (non-admin) JWT deleted product {pid}."
        )
