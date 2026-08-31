
# **Revoshop Database Design**
Database schema for the RevoShop e-commerce application (Checkpoint 1).
Designed to store users, categories, products, orders, and order_items data before any application code is written."

design and validate the database that will power the entire store: users, products, categories, orders, and the line items that link orders to products.

## Design tables for:

- ***users*** — account records.
- ***categories*** — product categories.
- ***products*** — store items, linked to a category.
- ***orders*** — placed by a user.
- ***order_items*** — junction table linking orders and products (many-to-many), with order_id and product_id as foreign keys.

### Local Setup Instructions

1. Ensure PostgreSQL is installed and its service is running.

2. Create the **`revoshop_db`** database:
   ```bash
   \CREATE DATABASE revoshop_db
   ```
3. Koneksikan database ke DBeaver / pgAdmin
4. Run the schema :
   Load Execute `schema.sql` file to create table first
5. Insert Sample data :
   input data sample from `seed.sql`
6. Run sample queries for verification :
   run `queries.sql` to validate the quearies

# ERD

See the relationship diagram between tables in ERD.png (ascreenshot from pgAdmin/dbeaver diagram).

![Schema Diagram](ERD.png)

## Notes

[POSTMAN LINK OF DOCUMENTATION]

https://documenter.getpostman.com/view/57336695/2sBYAuTXQT

## How to Run the Project Locally

### 1. Clone & buat virtual environment
```bash
git clone <url-repo-ini>
cd revoshop
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # macOS/Linux
```

### 2. Install dependency
```bash
pip install -r requirements.txt
```

### 3. Konfigurasi environment variable
Copy `.env.example` menjadi `.env`, lalu isi sesuai koneksi lokal Anda:
```
SQLALCHEMY_DATABASE_URI=postgresql://username:password@localhost:5432/revoshop_db
SECRET_KEY=<random-string-apa-saja>
DEBUG=True
```
> `.env` sudah masuk `.gitignore` — jangan pernah commit kredensial asli.

### 4. Jalankan migrasi database
```bash
set FLASK_APP=run.py          # Windows (gunakan `export` di macOS/Linux)
flask db upgrade
```
(Riwayat migrasi lengkap — termasuk migration awal dan migration penambahan kolom `role` secara terpisah — sudah ada di folder `migrations/` dari Checkpoint 2.)

### 5. Isi sample data
```bash
python seed.py
```
Mengisi users, categories, products, dan 1 order yang terhubung ke 2 produk sekaligus (bukti many-to-many). Kredensial login untuk testing akan tercetak di terminal.

### 6. Jalankan aplikasi
```bash
python run.py
```
Server berjalan di `http://127.0.0.1:5000`.
