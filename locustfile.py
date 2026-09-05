"""
Locust load test for the RevoShop API.

This simulates a realistic CUSTOMER journey through the store:
    browse products -> view a product -> place an order -> view the order

Usage:
    1. Make sure the server is running (e.g. `flask run`).
    2. Run Locust:
           locust -f locustfile.py --host http://localhost:5000
    3. Open http://localhost:8089, set the number of users and spawn rate.

    Headless (no UI, good for reports):
           locust -f locustfile.py --host http://localhost:5000 \
                  --users 50 --spawn-rate 5 --run-time 1m --headless
"""
import random
from locust import HttpUser, task, between


class ShopperUser(HttpUser):
    """Simulates a customer browsing the store and placing orders."""

    # Think-time between actions, mimicking a human reading pages.
    wait_time = between(1, 3)

    def on_start(self):
        """Runs once per virtual user when it starts.
        Fetch catalog + a valid user_id so later tasks have real data."""
        self.product_ids = []
        self.user_id = None

        resp = self.client.get("/products/", name="/products/ [list]")
        if resp.status_code == 200:
            # only keep products that still have stock, so orders can succeed
            self.product_ids = [p["id"] for p in resp.json() if p.get("stock", 0) > 0]

        resp = self.client.get("/users/", name="/users/ [list]")
        if resp.status_code == 200 and resp.json():
            self.user_id = resp.json()[0]["id"]

    # ---------- BROWSE (most frequent) ----------

    @task(5)
    def browse_products(self):
        self.client.get("/products/", name="/products/ [list]")

    @task(4)
    def view_product_detail(self):
        if not self.product_ids:
            return
        pid = random.choice(self.product_ids)
        # name= groups all /products/<id> under one stats row
        self.client.get(f"/products/{pid}", name="/products/:id [detail]")

    @task(2)
    def browse_categories(self):
        self.client.get("/category/", name="/category/ [list]")

    # ---------- THE CORE FLOW: place an order ----------

    @task(3)
    def place_order(self):
        """Simulate checkout: pick 1-3 products and place an order.
        The server computes total_amount from the real prices."""
        if not self.user_id or not self.product_ids:
            return

        # pick a few random products for the cart
        chosen = random.sample(
            self.product_ids, k=min(len(self.product_ids), random.randint(1, 3))
        )
        items = [{"product_id": pid, "quantity": random.randint(1, 2)} for pid in chosen]

        payload = {"user_id": self.user_id, "items": items}

        with self.client.post(
            "/orders/", json=payload, name="/orders/ [create]", catch_response=True
        ) as resp:
            if resp.status_code == 201:
                # follow the flow: view the order we just created
                order_id = resp.json().get("order", {}).get("id")
                if order_id:
                    self.client.get(f"/orders/{order_id}", name="/orders/:id [detail]")
            elif resp.status_code == 400 and "insufficient stock" in resp.text:
                # running out of stock under load is expected, not a real failure
                resp.success()
            else:
                resp.failure(f"Unexpected status {resp.status_code}: {resp.text}")

    @task(1)
    def view_orders(self):
        self.client.get("/orders/", name="/orders/ [list]")


class AuthUser(HttpUser):
    """A separate user type that stresses the login endpoint."""

    wait_time = between(2, 5)

    @task
    def login(self):
        # Adjust to match a user that exists in your database.
        self.client.post(
            "/auth/login",
            json={"email": "jokotest123@email.com", "password": "testpassword123"},
            name="/auth/login",
        )
