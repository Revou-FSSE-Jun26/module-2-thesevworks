"""Preservation property test — Property 2: Non-Bug Behavior Is Unchanged.

Spec: admin-role-protection (bugfix).
Requirements covered: 3.2, 3.3, 3.4, 3.5, 3.6.

This is the OBSERVATION-FIRST preservation suite. It documents the baseline
behavior for inputs that do NOT satisfy the bug condition — behavior that MUST
remain identical after the admin-role-protection fix (tasks 3.x) is applied.

    FOR ALL req WHERE NOT isBugCondition(req) DO
        ASSERT F'(req) == F(req)   # behavior preserved by the fix
    END FOR

Non-bug-condition inputs covered here:
  * Public catalog reads without a token stay 200 with the same data:
        GET /products/, GET /products/<id>, GET /category/, GET /category/<id>   (Req 3.4)
  * Login unchanged: valid credentials -> 200 + token whose identity is
        sub=str(user.id) and whose claims carry {email, role};
        invalid credentials -> 401 with the existing message.                     (Req 3.2, 3.3)
  * Registration unchanged: POST /users/ stays public, still hashes the password,
        and still runs field validation + the duplicate-email check
        (duplicate -> 409, short password -> 400, missing fields -> 400).          (Req 3.5, 3.6)
  * Orders unaffected: POST /orders/ (buyer checkout) still returns 201 because
        orders are out of scope for admin_required.                                (Req 3.6)

EXPECTED OUTCOME (pre-fix, unfixed code F): every test here PASSES. The suite
captures the current baseline so a regression introduced by the fix would be
caught. These assertions must reflect the TRUE current behavior — if one fails,
the assertion (not the application code) is corrected to match the real baseline.

The harness in tests/conftest.py seeds (session scope):
  * Category "Electronics"            (first/only category)
  * Products "Laptop", "Mechanical Keyboard"
  * Buyer user "Joko" <jokotest123@email.com> / password "testpassword123", role=buyer
  * 1 Order for Joko
Property-based coverage uses Hypothesis where it strengthens the guarantee across
the input domain, alongside concrete example-based unit tests.
"""

import pytest

from flask_jwt_extended import decode_token

from app import db as _db
from models import Product, Category, User


# Credentials of the buyer seeded by conftest.py — used to exercise login and checkout.
SEED_BUYER_EMAIL = "jokotest123@email.com"
SEED_BUYER_PASSWORD = "testpassword123"


# --- helpers -----------------------------------------------------------------

def _seed_product_and_category_ids(app):
    """Return (category_id, [product_ids]) from the seeded baseline data."""
    with app.app_context():
        category = Category.query.first()
        products = Product.query.order_by(Product.id).all()
        return category.id, [p.id for p in products]


# =============================================================================
# Req 3.4 — Public catalog reads stay 200 with the same data (no token)
# =============================================================================

def test_get_products_list_public_returns_200_with_seed_data(client):
    """GET /products/ without a token stays public and returns the seeded products.

    Validates: Requirements 3.4
    """
    resp = client.get("/products/")
    assert resp.status_code == 200
    body = resp.get_json()
    assert isinstance(body, list)
    names = {p["product_name"] for p in body}
    assert {"Laptop", "Mechanical Keyboard"}.issubset(names)


def test_get_product_by_id_public_returns_200_with_same_data(app, client):
    """GET /products/<id> without a token returns the same record as the DB holds.

    Validates: Requirements 3.4
    """
    with app.app_context():
        product = Product.query.order_by(Product.id).first()
        pid = product.id
        expected_name = product.product_name

    resp = client.get(f"/products/{pid}")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["id"] == pid
    assert body["product_name"] == expected_name


def test_get_product_by_id_unknown_returns_404(client):
    """Unknown product id still returns the existing 404 (public, no token)."""
    resp = client.get("/products/99999")
    assert resp.status_code == 404


def test_get_categories_list_public_returns_200_with_seed_data(client):
    """GET /category/ without a token stays public and lists the seeded category.

    Validates: Requirements 3.4
    """
    resp = client.get("/category/")
    assert resp.status_code == 200
    body = resp.get_json()
    assert isinstance(body, list)
    names = {c["category_name"] for c in body}
    assert "Electronics" in names


def test_get_category_by_id_public_returns_200_with_same_data(app, client):
    """GET /category/<id> without a token returns the same category as the DB holds.

    Validates: Requirements 3.4
    """
    with app.app_context():
        category = Category.query.first()
        cid = category.id
        expected_name = category.category_name

    resp = client.get(f"/category/{cid}")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["id"] == cid
    assert body["category_name"] == expected_name


# =============================================================================
# Req 3.2 / 3.3 — Login unchanged
# =============================================================================

def test_login_valid_credentials_returns_200_and_token(app, client):
    """Valid credentials -> 200 + a token whose identity is sub=str(user.id) and
    whose additional claims carry {email, role}.

    Validates: Requirements 3.2
    """
    resp = client.post("/auth/login", json={
        "email": SEED_BUYER_EMAIL,
        "password": SEED_BUYER_PASSWORD,
    })
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["success"] is True
    token = body["token"]
    assert token

    # Decode the token and verify the identity + claims shape is preserved.
    with app.app_context():
        decoded = decode_token(token)
        user = User.query.filter_by(email=SEED_BUYER_EMAIL).first()
        assert decoded["sub"] == str(user.id)
        assert decoded["email"] == SEED_BUYER_EMAIL
        assert decoded["role"] == user.role  # "buyer"


def test_login_invalid_password_returns_401_with_existing_message(client):
    """Invalid credentials -> 401 with the existing failure message.

    Validates: Requirements 3.3
    """
    resp = client.post("/auth/login", json={
        "email": SEED_BUYER_EMAIL,
        "password": "definitely-wrong-password",
    })
    assert resp.status_code == 401
    body = resp.get_json()
    assert body["success"] is False
    assert body["message"] == "wrong username/email/password"


def test_login_unknown_email_returns_401(client):
    """Unknown email -> 401 (existing behavior preserved).

    Validates: Requirements 3.3
    """
    resp = client.post("/auth/login", json={
        "email": "nobody-here@example.com",
        "password": "whatever123",
    })
    assert resp.status_code == 401
    assert resp.get_json()["success"] is False


# =============================================================================
# Req 3.5 / 3.6 — Registration stays public, hashes password, validates fields
# =============================================================================

def test_registration_public_creates_user_and_hashes_password(app, client):
    """POST /users/ stays public, returns 201, and the stored password is HASHED
    (never equal to the plaintext) and verifiable via check_password.

    Validates: Requirements 3.5
    """
    plaintext = "secret123"
    resp = client.post("/users/", json={
        "username": "PreserveReg",
        "email": "preserve_reg@example.com",
        "password": plaintext,
    })
    assert resp.status_code == 201
    created = resp.get_json()["user"]
    assert created["email"] == "preserve_reg@example.com"
    # New registrations default to the buyer role (preserved behavior).
    assert created["role"] == "buyer"

    with app.app_context():
        user = User.query.filter_by(email="preserve_reg@example.com").first()
        assert user is not None
        # Password must be stored hashed, not in plaintext.
        assert user.password_hash != plaintext
        assert user.check_password(plaintext) is True


def test_registration_duplicate_email_returns_409(client):
    """Duplicate email -> 409 with the existing message (duplicate-email check preserved).

    Validates: Requirements 3.5, 3.6
    """
    payload = {
        "username": "DupOne",
        "email": "dup_preserve@example.com",
        "password": "secret123",
    }
    first = client.post("/users/", json=payload)
    assert first.status_code == 201

    second = client.post("/users/", json={
        "username": "DupTwo",
        "email": "dup_preserve@example.com",
        "password": "secret123",
    })
    assert second.status_code == 409
    assert second.get_json()["error"] == "Email already registered"


def test_registration_short_password_returns_400(client):
    """Short password (< 6 chars) -> 400 with the existing message.

    Validates: Requirements 3.6
    """
    resp = client.post("/users/", json={
        "username": "ShortPw",
        "email": "shortpw_preserve@example.com",
        "password": "123",
    })
    assert resp.status_code == 400
    assert resp.get_json()["error"] == "Password must be at least 6 characters"


def test_registration_missing_fields_returns_400(client):
    """Missing required fields -> 400 (field validation preserved).

    Validates: Requirements 3.6
    """
    resp = client.post("/users/", json={"username": "OnlyName"})
    assert resp.status_code == 400
    assert "Missing required fields" in resp.get_json()["error"]


# =============================================================================
# Req 3.6 — Orders out of scope for admin_required (checkout stays 201)
# =============================================================================

def test_post_orders_buyer_checkout_returns_201(app, client):
    """POST /orders/ (buyer checkout) still returns 201 — orders are out of scope
    for admin_required, so no token is required and the order is created.

    Validates: Requirements 3.6
    """
    with app.app_context():
        buyer = User.query.filter_by(email=SEED_BUYER_EMAIL).first()
        user_id = buyer.id
        # Pick a product with enough stock for a single-unit checkout.
        product = Product.query.filter(Product.stock >= 1).order_by(Product.id).first()
        pid = product.id

    resp = client.post("/orders/", json={
        "user_id": user_id,
        "items": [{"product_id": pid, "quantity": 1}],
    })
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["status"] == "success"
    assert body["order"]["user_id"] == user_id


# =============================================================================
# Property-based preservation (Hypothesis) — stronger guarantees across inputs
# =============================================================================

try:
    from hypothesis import given, settings, HealthCheck, strategies as st

    _HAS_HYPOTHESIS = True
except ImportError:  # pragma: no cover - hypothesis optional
    _HAS_HYPOTHESIS = False


if _HAS_HYPOTHESIS:

    @settings(max_examples=25, deadline=None,
              suppress_health_check=[HealthCheck.function_scoped_fixture])
    @given(password=st.text(
        alphabet=st.characters(min_codepoint=33, max_codepoint=126),
        min_size=0, max_size=5,
    ))
    def test_registration_rejects_any_short_password(client, password):
        """PROPERTY: for any password shorter than 6 chars, POST /users/ returns
        400 with the existing message (field-validation preserved across inputs).

        Validates: Requirements 3.6
        """
        resp = client.post("/users/", json={
            "username": "PropShortPw",
            "email": "prop_shortpw@example.com",
            "password": password,
        })
        assert resp.status_code == 400
        assert resp.get_json()["error"] == "Password must be at least 6 characters"

    @settings(max_examples=25, deadline=None,
              suppress_health_check=[HealthCheck.function_scoped_fixture])
    @given(wrong_password=st.text(min_size=1, max_size=20).filter(
        lambda p: p != SEED_BUYER_PASSWORD))
    def test_login_rejects_any_wrong_password(client, wrong_password):
        """PROPERTY: for any password that is not the real one, login returns 401
        with the existing message (auth rejection preserved across inputs).

        Validates: Requirements 3.3
        """
        resp = client.post("/auth/login", json={
            "email": SEED_BUYER_EMAIL,
            "password": wrong_password,
        })
        assert resp.status_code == 401
        assert resp.get_json()["message"] == "wrong username/email/password"

    @settings(max_examples=15, deadline=None,
              suppress_health_check=[HealthCheck.function_scoped_fixture])
    @given(data=st.data())
    def test_public_catalog_reads_stay_200_without_token(client, app, data):
        """PROPERTY: public catalog read endpoints always return 200 without a token
        (public-read preservation across the real catalog endpoints).

        Validates: Requirements 3.4
        """
        endpoint = data.draw(st.sampled_from(["/products/", "/category/"]))
        resp = client.get(endpoint)
        assert resp.status_code == 200
        assert isinstance(resp.get_json(), list)
