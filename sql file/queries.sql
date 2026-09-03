-- 1. Create Users Table
CREATE TABLE users (
    id 				SERIAL PRIMARY KEY,
    username 		VARCHAR(100) NOT NULL,
    email 			VARCHAR(100) UNIQUE NOT NULL,
    password_hash 	VARCHAR(50) NOT NULL,
    created_at 		TIMESTAMP DEFAULT NOW()
);

-- 3. Create Category Table
CREATE TABLE category (
    id             	SERIAL PRIMARY KEY,
    category_name   VARCHAR(50) NOT NULL,
    description    	TEXT,
    created_at     	TIMESTAMP DEFAULT NOW()
);

-- 3. Create Products Table
CREATE TABLE products (
    id             	SERIAL PRIMARY KEY,
    category_id		INT NOT NULL REFERENCES category(id),
    product_name	VARCHAR(50) NOT NULL,
    description    	TEXT,
    price          	NUMERIC(10,2) NOT NULL,
    stock 			INTEGER NOT NULL,
    created_at     	TIMESTAMP DEFAULT NOW()
);

-- 4. Create Orders Table
CREATE TABLE orders (
    id 				SERIAL PRIMARY KEY,
    user_id 		INT NOT NULL REFERENCES users(id),
    total_amount 	NUMERIC(15, 2) NOT NULL,
    status 			VARCHAR(20) NOT NULL,
    ordered_at 		TIMESTAMP DEFAULT NOW()
);

-- 5. Create Order Items Table (Junction orders & products)
CREATE TABLE order_items (
    id 						SERIAL PRIMARY KEY,
    order_id 				INT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id 				INT NOT NULL REFERENCES products(id) ON DELETE restrict,
	quantity 				INT NOT NULL DEFAULT 1,
	price_at_purchase 		NUMERIC(10,2) NOT NULL
);




-- REVOSHOP SEED DATA SAMPLE
-- Realistic & varied sample data for e-commerce-style schema
-- =========================================================

-- ---------------------------------------------------------
-- 1. Users
-- ---------------------------------------------------------
INSERT INTO users (username, email, password_hash, created_at) VALUES
('budi_santoso',    'budi.santoso@gmail.com',    'password123', '2024-01-15 08:23:11'),
('siti_rahma',      'siti.rahma@yahoo.com',      'siti12345',   '2024-02-03 10:05:44'),
('andi_wijaya',     'andi.wijaya@outlook.com',   'andiw2024',   '2024-02-20 14:12:09'),
('dewi_lestari',    'dewi.lestari@gmail.com',    'dewipass1',   '2024-03-05 09:41:27'),
('rian_pratama',    'rian.pratama@gmail.com',    'rianp123',    '2024-03-18 16:55:03'),
('maya_kusuma',     'maya.kusuma@hotmail.com',   'mayakusuma',  '2024-04-02 11:30:52'),
('fajar_nugroho',   'fajar.nugroho@gmail.com',   'fajar2024',   '2024-04-19 07:18:39'),
('nadia_putri',     'nadia.putri@yahoo.com',     'nadiaputri1', '2024-05-01 13:47:15'),
('yusuf_hakim',     'yusuf.hakim@gmail.com',     'yusufhakim9', '2024-05-14 19:02:58'),
('lina_marlina',    'lina.marlina@outlook.com',  'linamarlina', '2024-06-08 12:00:00');

-- ---------------------------------------------------------
-- 2. Category
-- ---------------------------------------------------------
INSERT INTO category (category_name, description, created_at) VALUES
('Elektronik',      'Perangkat elektronik seperti gadget, aksesoris, dan komputer', '2024-01-10 08:00:00'),
('Fashion Pria',     'Pakaian, sepatu, dan aksesoris untuk pria',                    '2024-01-10 08:05:00'),
('Fashion Wanita',   'Pakaian, sepatu, dan aksesoris untuk wanita',                  '2024-01-10 08:10:00'),
('Rumah Tangga',     'Peralatan dan perlengkapan rumah tangga',                      '2024-01-10 08:15:00'),
('Olahraga',         'Peralatan dan perlengkapan olahraga',                          '2024-01-10 08:20:00'),
('Buku & Alat Tulis','Buku, alat tulis, dan perlengkapan kantor',                    '2024-01-10 08:25:00'),
('Makanan & Minuman','Produk makanan dan minuman kemasan',                           '2024-01-10 08:30:00');

-- ---------------------------------------------------------
-- 3. Products
-- ---------------------------------------------------------
INSERT INTO products (category_id, product_name, description, price, stock, created_at) VALUES
(1, 'Wireless Mouse Logitech',   'Mouse nirkabel dengan sensor optik presisi tinggi',       125000.00,  85, '2024-01-20 09:00:00'),
(1, 'Headset Bluetooth JBL',     'Headset bluetooth dengan noise cancelling',               450000.00,  40, '2024-01-22 10:15:00'),
(1, 'Power Bank 10000mAh',       'Power bank fast charging kapasitas 10000mAh',             175000.00, 120, '2024-01-25 11:30:00'),
(1, 'Kabel USB Type-C 1M',       'Kabel data dan charging USB Type-C panjang 1 meter',       35000.00, 300, '2024-01-28 08:45:00'),
(2, 'Kemeja Flanel Pria',        'Kemeja flanel lengan panjang bahan katun',                 189000.00,  60, '2024-02-02 09:20:00'),
(2, 'Celana Chino Slim Fit',     'Celana chino slim fit warna khaki',                        215000.00,  45, '2024-02-05 13:10:00'),
(2, 'Sepatu Sneakers Pria',      'Sepatu sneakers casual bahan kanvas',                      329000.00,  30, '2024-02-10 15:00:00'),
(3, 'Dress Wanita Motif Bunga',  'Dress casual motif bunga bahan katun rayon',               199000.00,  55, '2024-02-14 10:30:00'),
(3, 'Tas Selempang Wanita',      'Tas selempang kulit sintetis ukuran medium',               159000.00,  70, '2024-02-18 14:20:00'),
(4, 'Blender Portable',          'Blender mini portable rechargeable',                       210000.00,  25, '2024-03-01 08:00:00'),
(4, 'Rice Cooker 1.8L',          'Rice cooker kapasitas 1.8 liter anti lengket',             385000.00,  18, '2024-03-04 09:30:00'),
(5, 'Matras Yoga Anti Slip',     'Matras yoga tebal 10mm anti slip',                          95000.00,  50, '2024-03-10 11:00:00'),
(5, 'Dumbbell Set 5kg',          'Set dumbbell besi lapis karet berat 5kg per unit',         275000.00,  22, '2024-03-15 16:40:00'),
(6, 'Novel Laskar Pelangi',      'Novel best seller karya Andrea Hirata',                     78000.00, 200, '2024-03-20 10:10:00'),
(6, 'Buku Tulis Sinar Dunia (1 Lusin)', 'Buku tulis isi 38 lembar, satu lusin',               45000.00, 150, '2024-03-22 09:00:00'),
(7, 'Kopi Bubuk Gayo 250gr',     'Kopi bubuk arabika asal Gayo kemasan 250gr',                65000.00,  90, '2024-04-01 08:30:00'),
(7, 'Keripik Singkong Pedas',    'Keripik singkong renyah rasa pedas manis',                  18000.00, 250, '2024-04-03 10:00:00');

-- ---------------------------------------------------------
-- 4. Orders
-- (total_amount recalculated to match order_items below,
--  including quantity)
-- ---------------------------------------------------------
INSERT INTO orders (user_id, total_amount, status, ordered_at) VALUES
(1,  625000.00, 'completed',  '2024-05-02 10:15:00'),
(2,  199000.00, 'completed',  '2024-05-04 14:22:00'),
(3,  593000.00, 'shipped',    '2024-05-10 09:05:00'),
(4,  385000.00, 'completed',  '2024-05-12 16:47:00'),
(1,  144000.00, 'cancelled',  '2024-05-15 11:30:00'),
(5,  329000.00, 'completed',  '2024-05-18 13:12:00'),
(6,  399000.00, 'shipped',    '2024-05-20 08:55:00'),
(7,  159000.00, 'pending',    '2024-05-22 17:40:00'),
(8,  477000.00, 'completed',  '2024-05-25 12:00:00'),
(9,  585000.00, 'pending',    '2024-05-28 15:20:00'),
(2,  246000.00, 'completed',  '2024-06-01 09:45:00'),
(10, 275000.00, 'shipped',    '2024-06-03 11:10:00'),
(3,  215000.00, 'completed',  '2024-06-07 10:00:00');

-- ---------------------------------------------------------
-- 5. Order Items
-- price_at_purchase stores the product price at the time of order (so historical totals stay correct even if product's current price later changes)
-- ---------------------------------------------------------

INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase) VALUES
-- Order 1 (Budi, completed): Headset x1 + Power Bank x1 = 625.000
(1, 2, 1, 450000.00),
(1, 3, 1, 175000.00),
-- Order 2 (Siti, completed): Dress x1 = 199.000
(2, 8, 1, 199000.00),
-- Order 3 (Andi, shipped): Kemeja x2 + Celana Chino x1 = 593.000
(3, 5, 2, 189000.00),
(3, 6, 1, 215000.00),
-- Order 4 (Dewi, completed): Rice Cooker x1 = 385.000
(4, 11, 1, 385000.00),
-- Order 5 (Budi, cancelled): Buku Tulis x2 + Keripik x3 = 144.000
(5, 15, 2, 45000.00),
(5, 17, 3, 18000.00),
-- Order 6 (Rian, shipped): Sepatu Sneakers x1 + Kabel USB x2 = 399.000
(6, 7, 1, 329000.00),
(6, 4, 2, 35000.00),
-- Order 7 (Maya, pending): Blender x1 + Matras Yoga x2 = 400.000
(7, 10, 1, 210000.00),
(7, 12, 2, 95000.00),
-- Order 8 (Fajar, completed): Tas Selempang x3 = 477.000
(8, 9, 3, 159000.00),
-- Order 9 (Nadia, pending): Headset x1 + Kabel USB x2 + Kopi Bubuk x1 = 585.000
(9, 2, 1, 450000.00),
(9, 4, 2, 35000.00),
(9, 16, 1, 65000.00),
-- Order 10 (Yusuf, completed): Novel x2 + Keripik x5 = 246.000
(10, 14, 2, 78000.00),
(10, 17, 5, 18000.00),
-- Order 11 (Siti, shipped): Dumbbell Set x1 = 275.000
(11, 13, 1, 275000.00),
-- Order 12 (Lina, completed): Celana Chino x1 = 215.000
(12, 6, 1, 215000.00);

-------------------------------------------------------------------
--LIST OF SAMPLE QUERIES 

--Cari 5 produk termurah di kategori "Elektronik" yang stoknya masih tersedia:
SELECT product_name, price, stock
FROM products
WHERE category_id = 1 AND stock > 0
ORDER BY price ASC
LIMIT 5;

--List semua order beserta nama user yang memesan diatas 250.000:
SELECT 
 o.id AS order_id,
 u.username, 
 o.total_amount, 
 o.status
FROM orders o
JOIN users u on o.user_id = u.id
WHERE total_amount > 250000
ORDER BY total_amount DESC
LIMIT 10;


