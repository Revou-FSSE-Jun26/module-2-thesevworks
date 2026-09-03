import os
import pytest

# Point the app at a dedicated TEST database BEFORE importing app,
# so we never touch the development data.
os.environ.setdefault(
    "DATABASE_URL",
    "postgresql://postgres:supersev@localhost:5432/revoshop_test_db",
)
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key")

from app import app as flask_app, db as _db
from models import Product, Category, User, Order


@pytest.fixture(scope="session")
def app():
    flask_app.config.update(
        TESTING=True,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    with flask_app.app_context():
        _db.drop_all()
        _db.create_all()

        # --- seed baseline data ---
        category = Category(category_name="Electronics", description="Electronic devices")
        _db.session.add(category)
        _db.session.flush()  # get category.id

        product1 = Product(
            product_name="Laptop Gaming",
            description="High-end laptop",
            price=2999.99,
            stock=1,
            category_id=category.id,
        )
        product2 = Product(
            product_name="Webcam",
            description="HD webcam",
            price=99.99,
            stock=2,
            category_id=category.id,
        )
        _db.session.add_all([product1, product2])

        user = User(username="John", email="johntest123@email.com", role="buyer")
        user.hashing_password("testpassword123")
        _db.session.add(user)
        _db.session.flush()  # get user.id

        order = Order(user_id=user.id, total_amount=2999.99, status="pending")
        _db.session.add(order)

        _db.session.commit()

        yield flask_app

        _db.session.remove()
        _db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def db_session(app):
    """Provides a clean session; rolls back changes made within a test."""
    yield _db.session
    _db.session.rollback()
