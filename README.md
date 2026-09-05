# RevoShop API

**Live deployment:** https://sevoshop.onrender.com/

## 1. Overview

RevoShop is an online store REST API that powers the core of an e-commerce
application. It manages **users, products, categories, orders, and order items**
through a clean RESTful interface, backed by a **PostgreSQL** database.

Clients (a web front-end, a mobile app, or a tool like Postman) interact with the
store entirely over HTTP: browsing the product catalog, grouping products by
category, registering users, authenticating, and placing orders. Orders and
products share a **many-to-many** relationship expressed through an `order_items`
junction table, so a single order can contain multiple products and a product can
appear in many orders.

## 2. Features Implemented

- **Full CRUD for products** — create, read (list & by id), update (partial), and delete.
- **Full CRUD for categories** — create, read, update, and delete, with duplicate-name protection.
- **Full CRUD for orders** — create, read, update (status), and delete (soft delete via `is_deleted`).
- **Many-to-many relationship** between orders and products through the `order_items`
  table, where each row records the product, quantity, and price at purchase.
- **User management & authentication** — user creation with hashed passwords
  (Werkzeug), and a `/auth/login` endpoint that issues a JWT.
- **Data validation** on every write endpoint — required-field checks, type and
  range validation (e.g. price/stock cannot be negative), and email format checks.
- **Error handling** — every write operation is wrapped in `try/except` with
  `db.session.rollback()` on failure, returning meaningful HTTP status codes
  (400, 404, 409, 500) instead of crashing.
- **Deletion guard** — deleting a product that is still linked to active orders is
  blocked by the database foreign-key constraint (`order_items.product_id` uses
  `ON DELETE RESTRICT`), so referenced products cannot be removed and the error is
  caught and reported cleanly.

## 3. Technologies Used

| Category | Technology |
|----------|------------|
| Web framework | **Flask** |
| ORM | **SQLAlchemy** (Flask-SQLAlchemy) |
| Migrations | **Flask-Migrate** (Alembic) |
| Database | **PostgreSQL** |
| DB admin tools | **pgAdmin** / DBeaver |
| Authentication | **Flask-JWT-Extended** |
| Testing | **pytest** |
| Load testing | **Locust** |
| Config / secrets | **python-dotenv** |
| Production server | **gunicorn** |
| Deployment | Railway / Render / Heroku |

## 4. How to Run the Project Locally

### Prerequisites
- Python 3.10+
- PostgreSQL installed and its service running

### Step 1 — Clone the repository
```bash
git clone <url-repo-ini>
cd module-2-thesevworks
```

### Step 2 — Create and activate a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Create the database
In pgAdmin, DBeaver, or psql, create the database:
```sql
CREATE DATABASE revoshop_db;
```

### Step 5 — Configure environment variables
Copy the provided `.env.example` to `.env` and fill in your local connection details:
```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```
Then edit `.env`:
```
DATABASE_URL=postgresql://username:password@localhost:5432/revoshop_db
JWT_SECRET_KEY=change-me-to-a-random-string
```
> `.env` is already in `.gitignore` — never commit real credentials.

### Step 6 — Apply database migrations
Run all migrations to build the schema before starting the app:
```bash
# Windows
set FLASK_APP=app.py

# macOS / Linux
export FLASK_APP=app.py

flask db upgrade
```
The complete migration history — including the initial schema and the later
`is_deleted` column addition — lives in the `migrations/` folder.

### Step 7 — (Optional) Seed sample data
```bash
python seed.py
```
This inserts users, categories, products, and an order linked to multiple products
(demonstrating the many-to-many relationship).

### Step 8 — Run the application
```bash
flask run
```
The server starts at `http://127.0.0.1:5000`.

---

## Testing

Run the automated test suite with pytest:
```bash
pytest -v
```
The tests run against a dedicated `revoshop_test_db` database (create it once with
`CREATE DATABASE revoshop_test_db;`) so your development data is never touched.

![pytest screenshot](Snapshot/Pytest_Check.png)


## Load Testing

Start the server, then in another terminal run Locust:
```bash
locust -f locustfile.py --host http://localhost:5000
```
Open `http://localhost:8089` to configure the number of virtual users and start the test.

---

## Database Design

The schema stores five entities:

- **users** — account records (with hashed passwords and a role).
- **category** — product categories.
- **products** — store items, each linked to a category.
- **orders** — placed by a user, with a total amount and status.
- **order_items** — junction table linking orders and products (many-to-many),
  with `order_id` and `product_id` as foreign keys plus quantity and price at purchase.

### ERD
See the relationship diagram between tables in `Snapshot/ERD.png` (a screenshot from the
pgAdmin/DBeaver diagram).

![Schema Diagram](Snapshot/ERD.png)

## API Documentation

Full endpoint documentation is available on Postman:

https://documenter.getpostman.com/view/57336695/2sBYAuTXQT
