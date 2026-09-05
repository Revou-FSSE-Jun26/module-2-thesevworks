"""
Locust load test untuk RevoShop API.

Cara pakai:
    1. Pastikan server berjalan (mis. `flask run` atau via gunicorn).
    2. Jalankan Locust:
           locust -f locustfile.py --host http://localhost:5000
    3. Buka http://localhost:8089 di browser, isi jumlah user & spawn rate.

    Atau headless (tanpa UI):
           locust -f locustfile.py --host http://localhost:5000 \
                  --users 50 --spawn-rate 5 --run-time 1m --headless
"""
import random
from locust import HttpUser, task, between


class RevoShopUser(HttpUser):
    # Jeda 1-3 detik antar task, meniru user yang membaca halaman.
    wait_time = between(1, 3)

    def on_start(self):
        """Dijalankan sekali per user virtual saat mulai.
        Ambil daftar produk & kategori supaya task lain punya id yang valid."""
        self.product_ids = []
        self.category_ids = []

        resp = self.client.get("/products/", name="/products/ [list]")
        if resp.status_code == 200:
            self.product_ids = [p["id"] for p in resp.json()]

        resp = self.client.get("/category/", name="/category/ [list]")
        if resp.status_code == 200:
            self.category_ids = [c["id"] for c in resp.json()]

    # ---------- READ (paling sering) ----------

    @task(5)
    def browse_products(self):
        self.client.get("/products/", name="/products/ [list]")

    @task(4)
    def view_product_detail(self):
        if not self.product_ids:
            return
        pid = random.choice(self.product_ids)
        # name= mengelompokkan semua /products/<id> jadi satu baris statistik
        self.client.get(f"/products/{pid}", name="/products/:id [detail]")

    @task(3)
    def browse_categories(self):
        self.client.get("/category/", name="/category/ [list]")

    @task(2)
    def view_orders(self):
        self.client.get("/orders/", name="/orders/ [list]")

    # ---------- WRITE (lebih jarang) ----------

    @task(1)
    def create_product(self):
        if not self.category_ids:
            return
        payload = {
            "category_id": random.choice(self.category_ids),
            "product_name": f"LoadTest-{random.randint(1, 100000)}",
            "description": "created by locust",
            "price": round(random.uniform(10, 500), 2),
            "stock": random.randint(1, 100),
        }
        resp = self.client.post("/products/", json=payload, name="/products/ [create]")
        # Simpan id baru supaya bisa dipakai task detail berikutnya
        if resp.status_code == 201:
            new_id = resp.json().get("product", {}).get("id")
            if new_id:
                self.product_ids.append(new_id)


class AuthUser(HttpUser):
    """User terpisah yang fokus menguji endpoint login."""
    wait_time = between(2, 5)

    @task
    def login(self):
        # Sesuaikan kredensial dengan user yang ada di database-mu.
        self.client.post(
            "/auth/login",
            json={"email": "jokotest123@email.com", "password": "testpassword123"},
            name="/auth/login",
        )
