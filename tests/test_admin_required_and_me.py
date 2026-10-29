"""Unit tests for the `admin_required` decorator and the `GET /auth/me` endpoint.

Spec: admin-role-protection (bugfix) — Task 3.6.
Requirements covered: 2.3 (admin_required enforcement), 2.6 (GET /auth/me).

These are standard unit tests that exercise the FIXED code:

`admin_required` (tested through a real guarded route, GET /users/):
    - No token            -> 401, and the handler does not run (no side effect / no data leak).
    - Buyer (non-admin)   -> 403 with body {"error": "Admin privileges required"}, no side effect.
    - Admin token         -> handler runs and returns its normal success (200 + a list).

`GET /auth/me`:
    - No token                       -> 401.
    - Valid buyer token              -> 200, body includes role == "buyer" with correct email/id.
    - Valid token, user deleted/gone -> 404 {"error": "User not found"}.

Shared-session-DB note: the `app` fixture in conftest.py is session-scoped and seeds a
single database shared by every test module. To avoid clashes we create our admin user
with a UNIQUE email and resolve the seeded buyer ("Joko") by its known email.
"""

import pytest

from app import db as _db
from models import User
from flask_jwt_extended import create_access_token


# --- constants / helpers -----------------------------------------------------

# Seeded buyer from conftest.py.
BUYER_EMAIL = "jokotest123@email.com"
BUYER_PASSWORD = "testpassword123"

# Unique admin identity for this module (avoid clashing with other modules'
# users on the shared session DB).
ADMIN_USERNAME = "AdminForUnitTest"
ADMIN_EMAIL = "admin_unit_me_test@example.com"
ADMIN_PASSWORD = "adminpassword123"


def _bearer(token):
    return {"Authorization": f"Bearer {token}"}


def _login(client, email, password):
    """Log in through the real endpoint and return the issued JWT.

    The token carries the production claims (identity=str(user.id),
    additional_claims {email, role}).
    """
    resp = client.post("/auth/login", json={"email": email, "password": password})
    assert resp.status_code == 200, (
        f"login harness precondition failed for {email}: "
        f"{resp.status_code} {resp.get_json()}"
    )
    return resp.get_json()["token"]


def _ensure_admin(app):
    """Create an admin user directly via the model (no admin is seeded).

    Returns (admin_id, admin_email). Idempotent on the shared session DB: if the
    admin already exists (e.g. test re-run within the same session) it is reused.
    """
    with app.app_context():
        admin = User.query.filter_by(email=ADMIN_EMAIL).first()
        if admin is None:
            admin = User(username=ADMIN_USERNAME, email=ADMIN_EMAIL, role="admin")
            admin.hashing_password(ADMIN_PASSWORD)
            _db.session.add(admin)
            _db.session.commit()
        assert admin.role == "admin"
        return admin.id, admin.email


def _buyer_token(client):
    return _login(client, BUYER_EMAIL, BUYER_PASSWORD)


def _admin_token(app, client):
    _ensure_admin(app)
    return _login(client, ADMIN_EMAIL, ADMIN_PASSWORD)


# --- admin_required: no token -----------------------------------------------

def test_admin_required_without_token_returns_401_and_handler_does_not_run(app, client):
    """No Authorization header -> 401; the guarded handler must not run.

    We assert the handler did not run by confirming the user list is NOT leaked:
    a 401 body never contains the list that GET /users/ would return.
    Requirements: 2.3.
    """
    resp = client.get("/users/")

    assert resp.status_code == 401, (
        f"expected 401 without a token, got {resp.status_code}: {resp.get_json()}"
    )
    # Handler did not run: response is not the success list of users.
    body = resp.get_json()
    assert not isinstance(body, list), (
        "handler appears to have run: GET /users/ returned a list without a token"
    )


# --- admin_required: buyer token --------------------------------------------

def test_admin_required_with_buyer_token_returns_403_with_message_and_no_side_effect(app, client):
    """Valid buyer JWT -> 403 with the exact admin-required message; handler skipped.

    Requirements: 2.3.
    """
    token = _buyer_token(client)

    resp = client.get("/users/", headers=_bearer(token))

    assert resp.status_code == 403, (
        f"expected 403 for a buyer token, got {resp.status_code}: {resp.get_json()}"
    )
    body = resp.get_json()
    assert body == {"error": "Admin privileges required"}, (
        f"unexpected 403 body: {body!r}"
    )
    # No side effect: handler did not run, so no user list leaked.
    assert not isinstance(body, list)


# --- admin_required: admin token --------------------------------------------

def test_admin_required_with_admin_token_runs_handler_and_returns_200_list(app, client):
    """Valid admin JWT -> handler runs; GET /users/ returns 200 with a list.

    Requirements: 2.3.
    """
    token = _admin_token(app, client)

    resp = client.get("/users/", headers=_bearer(token))

    assert resp.status_code == 200, (
        f"expected 200 for an admin token, got {resp.status_code}: {resp.get_json()}"
    )
    body = resp.get_json()
    assert isinstance(body, list), f"expected a list of users, got {type(body)}: {body!r}"
    # Sanity: the seeded buyer should appear in the admin-only listing.
    emails = {u.get("email") for u in body}
    assert BUYER_EMAIL in emails, f"seeded buyer missing from user list: {emails}"


# --- GET /auth/me: no token --------------------------------------------------

def test_me_without_token_returns_401(client):
    """GET /auth/me with no token -> 401 (jwt_required enforced).

    Requirements: 2.6.
    """
    resp = client.get("/auth/me")
    assert resp.status_code == 401, (
        f"expected 401 without a token, got {resp.status_code}: {resp.get_json()}"
    )


# --- GET /auth/me: valid buyer token ----------------------------------------

def test_me_with_valid_buyer_token_returns_profile_with_role(app, client):
    """GET /auth/me with a valid buyer token -> 200 with the correct profile.

    Body must include role == "buyer" and the correct email/id resolved from the
    JWT identity.
    Requirements: 2.6.
    """
    # Resolve the seeded buyer's id for cross-checking the response.
    with app.app_context():
        buyer = User.query.filter_by(email=BUYER_EMAIL).first()
        assert buyer is not None, "seed precondition: buyer Joko exists"
        buyer_id = buyer.id

    token = _buyer_token(client)

    resp = client.get("/auth/me", headers=_bearer(token))

    assert resp.status_code == 200, (
        f"expected 200 for a valid token, got {resp.status_code}: {resp.get_json()}"
    )
    body = resp.get_json()
    assert body.get("role") == "buyer", f"expected role 'buyer', got {body.get('role')!r}"
    assert body.get("email") == BUYER_EMAIL, f"wrong email in profile: {body.get('email')!r}"
    assert body.get("id") == buyer_id, f"wrong id in profile: {body.get('id')!r} != {buyer_id}"


# --- GET /auth/me: valid token but user no longer exists ---------------------

def test_me_with_token_for_nonexistent_user_returns_404(app, client):
    """GET /auth/me with a valid-looking token whose identity resolves to no user
    -> 404 {"error": "User not found"}.

    We mint a token for a non-existent id (999999) with proper claims inside an
    app_context, simulating a user that was deleted after the token was issued.
    Requirements: 2.6.
    """
    with app.app_context():
        # Guard: ensure id 999999 truly does not exist.
        assert User.query.get(999999) is None, "precondition: user 999999 must not exist"
        token = create_access_token(
            identity=str(999999),
            additional_claims={"email": "ghost@example.com", "role": "buyer"},
        )

    resp = client.get("/auth/me", headers=_bearer(token))

    assert resp.status_code == 404, (
        f"expected 404 for a token with no matching user, got {resp.status_code}: "
        f"{resp.get_json()}"
    )
    assert resp.get_json() == {"error": "User not found"}, (
        f"unexpected 404 body: {resp.get_json()!r}"
    )
