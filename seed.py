#!/usr/bin/env python3
"""
seed.py — Python equivalent of seed.sql

Recreates the same schema/data as the original PostgreSQL dump, but with
each table's sample data expanded up to 25 rows (category is expanded to
10 since it's a small lookup table).

Usage:
    pip install psycopg2-binary
    export DATABASE_URL="postgresql://user:password@localhost:5432/dbname"
    python seed.py

The script is idempotent: it creates the tables if they don't exist,
truncates them, reloads the sample data, and resets the sequences —
same end result as running the original seed.sql dump.
"""

import os
import sys
from datetime import datetime

import psycopg2
from psycopg2.extras import execute_values

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:supersev@localhost:5432/revoshop_db"
)

# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

DDL = """
CREATE TABLE IF NOT EXISTS alembic_version (
    version_num VARCHAR(32) NOT NULL PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(100) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'buyer'
);

CREATE TABLE IF NOT EXISTS category (
    id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES category(id),
    product_name VARCHAR(150) NOT NULL,
    description TEXT,
    price NUMERIC(12, 2) NOT NULL,
    stock INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    total_amount NUMERIC(12, 2) NOT NULL,
    status VARCHAR(20) NOT NULL,
    ordered_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    price_at_purchase NUMERIC(12, 2) NOT NULL
);
"""

TRUNCATE = """
TRUNCATE TABLE order_items, orders, products, category, users, alembic_version
RESTART IDENTITY CASCADE;
"""

# ---------------------------------------------------------------------------
# Sample data (25 rows per table, 10 for category)
# ---------------------------------------------------------------------------

ALEMBIC_VERSION = [("e298ff03ef56",)]

CATEGORY = [
    (1, "Elektronik", "Perangkat elektronik seperti gadget, aksesoris, dan komputer", "2024-01-10 08:00:00"),
    (2, "Fashion Pria", "Pakaian, sepatu, dan aksesoris untuk pria", "2024-01-10 08:05:00"),
    (3, "Fashion Wanita", "Pakaian, sepatu, dan aksesoris untuk wanita", "2024-01-10 08:10:00"),
    (4, "Rumah Tangga", "Peralatan dan perlengkapan rumah tangga", "2024-01-10 08:15:00"),
    (5, "Olahraga", "Peralatan dan perlengkapan olahraga", "2024-01-10 08:20:00"),
    (6, "Buku & Alat Tulis", "Buku, alat tulis, dan perlengkapan kantor", "2024-01-10 08:25:00"),
    (7, "Makanan & Minuman", "Produk makanan dan minuman kemasan", "2024-01-10 08:30:00"),
    (8, "Kesehatan & Kecantikan", "Produk kesehatan, suplemen, dan perawatan tubuh", "2024-01-10 08:35:00"),
    (9, "Otomotif", "Sparepart dan aksesoris kendaraan bermotor", "2024-01-10 08:40:00"),
    (10, "Mainan & Hobi", "Mainan, action figure, dan perlengkapan hobi", "2024-01-10 08:45:00"),
]

# sample data for POST create new Category
#     (11, "Make Up", "Produk perawatan wajah dan make up", "2024-01-10 08:50:00"),
#     (12, "Perlengkapan Bayi","Popok, susu formula, dan perlengkapan bayi lainnya", "2024-01-10 08:55:00"),
#     (13, "Perhiasan & Aksesoris", "Perhiasan emas, perak, dan permata", "2024-01-10 08:50:00"),
#     (14, "Kamera & Foto", "Kamera digital dan aksesori fotografi", "2024-01-10 09:15:00"),
#     (15, "Furniture", "Perabotan rumah dan furniture kayu", "2024-01-10 09:20:00"),
#  ]





USERS = [
    (1, "budi_santoso", "budi.santoso@gmail.com", "password123", "2024-01-15 08:23:11", "buyer"),
    (2, "siti_rahma", "siti.rahma@yahoo.com", "siti12345", "2024-02-03 10:05:44", "buyer"),
    (3, "andi_wijaya", "andi.wijaya@outlook.com", "andiw2024", "2024-02-20 14:12:09", "buyer"),
    (4, "dewi_lestari", "dewi.lestari@gmail.com", "dewipass1", "2024-03-05 09:41:27", "buyer"),
    (5, "rian_pratama", "rian.pratama@gmail.com", "rianp123", "2024-03-18 16:55:03", "buyer"),
    (6, "maya_kusuma", "maya.kusuma@hotmail.com", "mayakusuma", "2024-04-02 11:30:52", "buyer"),
    (7, "fajar_nugroho", "fajar.nugroho@gmail.com", "fajar2024", "2024-04-19 07:18:39", "buyer"),
    (8, "nadia_putri", "nadia.putri@yahoo.com", "nadiaputri1", "2024-05-01 13:47:15", "buyer"),
    (9, "yusuf_hakim", "yusuf.hakim@gmail.com", "yusufhakim9", "2024-05-14 19:02:58", "buyer"),
    (10, "lina_marlina", "lina.marlina@outlook.com", "linamarlina", "2024-06-08 12:00:00", "buyer"),
    (11, "hendra_saputra", "hendra.saputra@gmail.com", "hendras11", "2024-06-12 09:15:00", "buyer"),
    (12, "ratna_sari", "ratna.sari@yahoo.com", "ratnasari12", "2024-06-15 10:20:00", "buyer"),
    (13, "agus_setiawan", "agus.setiawan@gmail.com", "agus2024s", "2024-06-20 08:40:00", "buyer"),
    (14, "wulan_dari", "wulan.dari@outlook.com", "wulandari14", "2024-06-25 14:05:00", "buyer"),
    (15, "bayu_firmansyah", "bayu.firmansyah@gmail.com", "bayuf2024", "2024-07-01 11:10:00", "buyer"),
    (16, "citra_ayu", "citra.ayu@yahoo.com", "citraayu16", "2024-07-05 09:30:00", "buyer"),
    (17, "dimas_prasetyo", "dimas.prasetyo@gmail.com", "dimasp17", "2024-07-10 13:50:00", "buyer"),
    (18, "eka_novita", "eka.novita@hotmail.com", "ekanovita18", "2024-07-14 15:25:00", "buyer"),
    (19, "farhan_maulana", "farhan.maulana@gmail.com", "farhanm19", "2024-07-19 10:00:00", "buyer"),
    (20, "gita_permata", "gita.permata@yahoo.com", "gitap2024", "2024-07-24 12:15:00", "buyer"),
]
# sample data for POST create new Users route
#     (21, "admin_master", "admin.master@marketplace.com", "adminmaster", "2024-07-29 08:05:00", "admin"),
#     (22, "skincare_glow", "skincare.glow@outlook.com", "skincareglow", "2024-08-02 14:40:00", "seller"),
#     (23, "admin_support", "admin.support@marketplace.com", "adminsupport", "2024-08-07 09:55:00", "admin"),
#     (24, "toko_elektro", "toko.elektro@gmail.com", "tokoelektro", "2024-03-01 09:15:00", "seller"),
#     (25, "buku_cerdas", "buku.cerdas@gmail.com", "bukucerdas25", "2024-08-12 11:20:00", "seller"),
#  ]

PRODUCTS = [
    (1, 1, "Wireless Mouse Logitech", "Mouse nirkabel dengan sensor optik presisi tinggi", 125000.00, 85, "2024-01-20 09:00:00"),
    (2, 1, "Headset Bluetooth JBL", "Headset bluetooth dengan noise cancelling", 450000.00, 40, "2024-01-22 10:15:00"),
    (3, 1, "Power Bank 10000mAh", "Power bank fast charging kapasitas 10000mAh", 175000.00, 120, "2024-01-25 11:30:00"),
    (4, 1, "Kabel USB Type-C 1M", "Kabel data dan charging USB Type-C panjang 1 meter", 35000.00, 300, "2024-01-28 08:45:00"),
    (5, 2, "Kemeja Flanel Pria", "Kemeja flanel lengan panjang bahan katun", 189000.00, 60, "2024-02-02 09:20:00"),
    (6, 2, "Celana Chino Slim Fit", "Celana chino slim fit warna khaki", 215000.00, 45, "2024-02-05 13:10:00"),
    (7, 2, "Sepatu Sneakers Pria", "Sepatu sneakers casual bahan kanvas", 329000.00, 30, "2024-02-10 15:00:00"),
    (8, 3, "Dress Wanita Motif Bunga", "Dress casual motif bunga bahan katun rayon", 199000.00, 55, "2024-02-14 10:30:00"),
    (9, 3, "Tas Selempang Wanita", "Tas selempang kulit sintetis ukuran medium", 159000.00, 70, "2024-02-18 14:20:00"),
    (10, 4, "Blender Portable", "Blender mini portable rechargeable", 210000.00, 25, "2024-03-01 08:00:00"),
    (11, 4, "Rice Cooker 1.8L", "Rice cooker kapasitas 1.8 liter anti lengket", 385000.00, 18, "2024-03-04 09:30:00"),
    (12, 5, "Matras Yoga Anti Slip", "Matras yoga tebal 10mm anti slip", 95000.00, 50, "2024-03-10 11:00:00"),
    (13, 5, "Dumbbell Set 5kg", "Set dumbbell besi lapis karet berat 5kg per unit", 275000.00, 22, "2024-03-15 16:40:00"),
    (14, 6, "Novel Laskar Pelangi", "Novel best seller karya Andrea Hirata", 78000.00, 200, "2024-03-20 10:10:00"),
    (15, 6, "Buku Tulis Sinar Dunia (1 Lusin)", "Buku tulis isi 38 lembar, satu lusin", 45000.00, 150, "2024-03-22 09:00:00"),
    (16, 7, "Kopi Bubuk Gayo 250gr", "Kopi bubuk arabika asal Gayo kemasan 250gr", 65000.00, 90, "2024-04-01 08:30:00"),
    (17, 7, "Keripik Singkong Pedas", "Keripik singkong renyah rasa pedas manis", 18000.00, 250, "2024-04-03 10:00:00"),
    (18, 8, "Vitamin C 1000mg (30 Tablet)", "Suplemen vitamin C untuk daya tahan tubuh", 85000.00, 100, "2024-04-10 09:00:00"),
    (19, 8, "Sunscreen SPF50 PA+++", "Tabir surya untuk wajah, tekstur ringan", 120000.00, 75, "2024-04-12 10:30:00"),
    (20, 9, "Kampas Rem Motor Matic", "Kampas rem depan untuk motor matic universal", 65000.00, 60, "2024-04-15 08:15:00"),
]
# sample data for POST create new Products route:
    # (21, 9, "Minyak Pelumas Mesin 1L", "Oli mesin motor kemasan 1 liter", 55000.00, 90, "2024-04-18 09:45:00"),
    # (22, 10, "Action Figure Superhero", "Action figure koleksi bahan PVC tinggi 15cm", 145000.00, 40, "2024-04-20 11:00:00"),
    # (23, 10, "Puzzle 500 Keping", "Puzzle gambar pemandangan 500 keping", 65000.00, 55, "2024-04-22 13:20:00"),
    # (24, 1, "Keyboard Mechanical RGB", "Keyboard gaming mechanical dengan lampu RGB", 385000.00, 35, "2024-04-25 14:10:00"),
    # (25, 4, "Setrika Uap Portable", "Setrika uap portable anti lengket", 165000.00, 45, "2024-04-28 10:50:00"), 


ORDERS = [
    (1, 1, 625000.00, "completed", "2024-05-02 10:15:00"),
    (2, 2, 199000.00, "completed", "2024-05-04 14:22:00"),
    (3, 3, 593000.00, "shipped", "2024-05-10 09:05:00"),
    (4, 4, 385000.00, "completed", "2024-05-12 16:47:00"),
    (5, 1, 144000.00, "cancelled", "2024-05-15 11:30:00"),
    (6, 5, 329000.00, "completed", "2024-05-18 13:12:00"),
    (7, 6, 399000.00, "shipped", "2024-05-20 08:55:00"),
    (8, 7, 159000.00, "pending", "2024-05-22 17:40:00"),
    (9, 8, 477000.00, "completed", "2024-05-25 12:00:00"),
    (10, 9, 585000.00, "pending", "2024-05-28 15:20:00"),
    (11, 2, 246000.00, "completed", "2024-06-01 09:45:00"),
    (12, 10, 275000.00, "shipped", "2024-06-03 11:10:00"),
    (13, 3, 215000.00, "completed", "2024-06-07 10:00:00"),
    (14, 11, 233000.00, "completed", "2024-06-10 09:00:00"),
    (15, 12, 424000.00, "shipped", "2024-06-12 11:15:00"),
    (16, 13, 96000.00, "completed", "2024-06-14 14:30:00"),
    (17, 14, 490000.00, "pending", "2024-06-16 08:45:00"),
    (18, 15, 175000.00, "completed", "2024-06-18 10:20:00"),
    (19, 16, 305000.00, "shipped", "2024-06-20 13:05:00"),
    (20, 17, 65000.00, "cancelled", "2024-06-22 09:30:00"),
]
# sample data for POST create new Orders route :
#     (21, 18, 420000.00, "completed", "2024-06-24 15:40:00"),
#     (22, 19, 177000.00, "pending", "2024-06-26 11:50:00"),
#     (23, 20, 65000.00, "completed", "2024-06-28 08:10:00"),
#     (24, 21, 329000.00, "shipped", "2024-06-30 12:25:00"),
#     (25, 22, 138000.00, "completed", "2024-07-02 14:00:00"),
# ] 

ORDER_ITEMS = [
    (1, 1, 2, 1, 450000.00),
    (2, 1, 3, 1, 175000.00),
    (3, 2, 8, 1, 199000.00),
    (4, 3, 5, 2, 189000.00),
    (5, 3, 6, 1, 215000.00),
    (6, 4, 11, 1, 385000.00),
    (7, 5, 15, 2, 45000.00),
    (8, 5, 17, 3, 18000.00),
    (9, 6, 7, 1, 329000.00),
    (10, 6, 4, 2, 35000.00),
    (11, 7, 10, 1, 210000.00),
    (12, 7, 12, 2, 95000.00),
    (13, 8, 9, 3, 159000.00),
    (14, 9, 2, 1, 450000.00),
    (15, 9, 4, 2, 35000.00),
    (16, 9, 16, 1, 65000.00),
    (17, 10, 14, 2, 78000.00),
    (18, 10, 17, 5, 18000.00),
    (19, 11, 13, 1, 275000.00),
    (20, 12, 6, 1, 215000.00),
    (21, 14, 6, 1, 215000.00),
    (22, 14, 17, 1, 18000.00),
    (23, 15, 7, 1, 329000.00),
    (24, 15, 12, 1, 95000.00),
    (25, 16, 17, 2, 18000.00),
]
# sample data for POST create new Orders_items route : 
    # (26, 16, 14, 1, 78000.00),
    # (27, 17, 11, 1, 385000.00),
    # (28, 17, 4, 3, 35000.00),
    # (29, 18, 3, 1, 175000.00),
    # (30, 19, 10, 1, 210000.00),
    # (31, 19, 12, 1, 95000.00),
    # (32, 20, 16, 1, 65000.00),
    # (33, 21, 11, 1, 385000.00),
    # (34, 21, 4, 1, 35000.00),
    # (35, 22, 9, 1, 159000.00),
    # (36, 22, 17, 1, 18000.00),
    # (37, 23, 16, 1, 65000.00),
    # (38, 24, 7, 1, 329000.00),
    # (39, 25, 19, 1, 120000.00),
    # (40, 25, 17, 1, 18000.00),
# ]

# ---------------------------------------------------------------------------
# Seeding logic
# ---------------------------------------------------------------------------

SEQUENCES = [
    ("alembic_version", None),
    ("category_id_seq", ("category", "id", 10)),
    ("users_id_seq", ("users", "id", 20)),
    ("products_id_seq", ("products", "id", 20)),
    ("orders_id_seq", ("orders", "id", 20)),
    ("order_items_id_seq", ("order_items", "id", 25)),
]


def seed(conn):
    with conn.cursor() as cur:
        print("Creating schema (if not exists)...")
        cur.execute(DDL)

        print("Truncating existing data...")
        cur.execute(TRUNCATE)

        print("Inserting alembic_version...")
        execute_values(cur, "INSERT INTO alembic_version (version_num) VALUES %s", ALEMBIC_VERSION)

        print(f"Inserting {len(CATEGORY)} categories...")
        execute_values(
            cur,
            "INSERT INTO category (id, category_name, description, created_at) VALUES %s",
            CATEGORY,
        )

        print(f"Inserting {len(USERS)} users...")
        execute_values(
            cur,
            "INSERT INTO users (id, username, email, password_hash, created_at, role) VALUES %s",
            USERS,
        )

        print(f"Inserting {len(PRODUCTS)} products...")
        execute_values(
            cur,
            "INSERT INTO products (id, category_id, product_name, description, price, stock, created_at) VALUES %s",
            PRODUCTS,
        )

        print(f"Inserting {len(ORDERS)} orders...")
        execute_values(
            cur,
            "INSERT INTO orders (id, user_id, total_amount, status, ordered_at) VALUES %s",
            ORDERS,
        )

        print(f"Inserting {len(ORDER_ITEMS)} order_items...")
        execute_values(
            cur,
            "INSERT INTO order_items (id, order_id, product_id, quantity, price_at_purchase) VALUES %s",
            ORDER_ITEMS,
        )

        print("Resetting sequences...")
        for seq_name, info in SEQUENCES:
            if info is None:
                continue
            table, column, last_val = info
            cur.execute(
                f"SELECT setval(pg_get_serial_sequence(%s, %s), %s, true);",
                (table, column, last_val),
            )

    conn.commit()
    print("Done. Seeded: "
        f"{len(CATEGORY)} categories, {len(USERS)} users, {len(PRODUCTS)} products, "
        f"{len(ORDERS)} orders, {len(ORDER_ITEMS)} order_items.")


def main():
    try:
        conn = psycopg2.connect(DATABASE_URL)
    except psycopg2.OperationalError as exc:
        print(f"Could not connect to database at {DATABASE_URL!r}: {exc}", file=sys.stderr)
        sys.exit(1)

    try:
        seed(conn)
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
