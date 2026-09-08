--
-- PostgreSQL database dump
--

\restrict bQJbnJ7VKG2umhXET9TGqc4X28AA7KIA0pTQ2I0rrdnZpq1MebMqFndTqFfjV8L

-- Dumped from database version 18.4
-- Dumped by pg_dump version 18.4

-- Started on 2026-08-29 03:08:17

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 5055 (class 0 OID 17324)
-- Dependencies: 229
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.alembic_version VALUES ('e298ff03ef56');


--
-- TOC entry 5048 (class 0 OID 17175)
-- Dependencies: 222
-- Data for Name: category; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.categories VALUES (1, 'Elektronik', 'Perangkat elektronik seperti gadget, aksesoris, dan komputer', '2024-01-10 08:00:00');
INSERT INTO public.categories VALUES (2, 'Fashion Pria', 'Pakaian, sepatu, dan aksesoris untuk pria', '2024-01-10 08:05:00');
INSERT INTO public.categories VALUES (3, 'Fashion Wanita', 'Pakaian, sepatu, dan aksesoris untuk wanita', '2024-01-10 08:10:00');
INSERT INTO public.categories VALUES (4, 'Rumah Tangga', 'Peralatan dan perlengkapan rumah tangga', '2024-01-10 08:15:00');
INSERT INTO public.categories VALUES (5, 'Olahraga', 'Peralatan dan perlengkapan olahraga', '2024-01-10 08:20:00');
INSERT INTO public.categories VALUES (6, 'Buku & Alat Tulis', 'Buku, alat tulis, dan perlengkapan kantor', '2024-01-10 08:25:00');
INSERT INTO public.categories VALUES (7, 'Makanan & Minuman', 'Produk makanan dan minuman kemasan', '2024-01-10 08:30:00');


--
-- TOC entry 5046 (class 0 OID 17161)
-- Dependencies: 220
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.users VALUES (1, 'budi_santoso', 'budi.santoso@gmail.com', 'password123', '2024-01-15 08:23:11', 'buyer');
INSERT INTO public.users VALUES (2, 'siti_rahma', 'siti.rahma@yahoo.com', 'siti12345', '2024-02-03 10:05:44', 'buyer');
INSERT INTO public.users VALUES (3, 'andi_wijaya', 'andi.wijaya@outlook.com', 'andiw2024', '2024-02-20 14:12:09', 'buyer');
INSERT INTO public.users VALUES (4, 'dewi_lestari', 'dewi.lestari@gmail.com', 'dewipass1', '2024-03-05 09:41:27', 'buyer');
INSERT INTO public.users VALUES (5, 'rian_pratama', 'rian.pratama@gmail.com', 'rianp123', '2024-03-18 16:55:03', 'buyer');
INSERT INTO public.users VALUES (6, 'maya_kusuma', 'maya.kusuma@hotmail.com', 'mayakusuma', '2024-04-02 11:30:52', 'buyer');
INSERT INTO public.users VALUES (7, 'fajar_nugroho', 'fajar.nugroho@gmail.com', 'fajar2024', '2024-04-19 07:18:39', 'buyer');
INSERT INTO public.users VALUES (8, 'nadia_putri', 'nadia.putri@yahoo.com', 'nadiaputri1', '2024-05-01 13:47:15', 'buyer');
INSERT INTO public.users VALUES (9, 'yusuf_hakim', 'yusuf.hakim@gmail.com', 'yusufhakim9', '2024-05-14 19:02:58', 'buyer');
INSERT INTO public.users VALUES (10, 'lina_marlina', 'lina.marlina@outlook.com', 'linamarlina', '2024-06-08 12:00:00', 'buyer');


--
-- TOC entry 5052 (class 0 OID 17207)
-- Dependencies: 226
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.orders VALUES (1, 1, 625000.00, 'completed', '2024-05-02 10:15:00');
INSERT INTO public.orders VALUES (2, 2, 199000.00, 'completed', '2024-05-04 14:22:00');
INSERT INTO public.orders VALUES (3, 3, 593000.00, 'shipped', '2024-05-10 09:05:00');
INSERT INTO public.orders VALUES (4, 4, 385000.00, 'completed', '2024-05-12 16:47:00');
INSERT INTO public.orders VALUES (5, 1, 144000.00, 'cancelled', '2024-05-15 11:30:00');
INSERT INTO public.orders VALUES (6, 5, 329000.00, 'completed', '2024-05-18 13:12:00');
INSERT INTO public.orders VALUES (7, 6, 399000.00, 'shipped', '2024-05-20 08:55:00');
INSERT INTO public.orders VALUES (8, 7, 159000.00, 'pending', '2024-05-22 17:40:00');
INSERT INTO public.orders VALUES (9, 8, 477000.00, 'completed', '2024-05-25 12:00:00');
INSERT INTO public.orders VALUES (10, 9, 585000.00, 'pending', '2024-05-28 15:20:00');
INSERT INTO public.orders VALUES (11, 2, 246000.00, 'completed', '2024-06-01 09:45:00');
INSERT INTO public.orders VALUES (12, 10, 275000.00, 'shipped', '2024-06-03 11:10:00');
INSERT INTO public.orders VALUES (13, 3, 215000.00, 'completed', '2024-06-07 10:00:00');


--
-- TOC entry 5050 (class 0 OID 17187)
-- Dependencies: 224
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.products VALUES (1, 1, 'Wireless Mouse Logitech', 'Mouse nirkabel dengan sensor optik presisi tinggi', 125000.00, 85, '2024-01-20 09:00:00');
INSERT INTO public.products VALUES (2, 1, 'Headset Bluetooth JBL', 'Headset bluetooth dengan noise cancelling', 450000.00, 40, '2024-01-22 10:15:00');
INSERT INTO public.products VALUES (3, 1, 'Power Bank 10000mAh', 'Power bank fast charging kapasitas 10000mAh', 175000.00, 120, '2024-01-25 11:30:00');
INSERT INTO public.products VALUES (4, 1, 'Kabel USB Type-C 1M', 'Kabel data dan charging USB Type-C panjang 1 meter', 35000.00, 300, '2024-01-28 08:45:00');
INSERT INTO public.products VALUES (5, 2, 'Kemeja Flanel Pria', 'Kemeja flanel lengan panjang bahan katun', 189000.00, 60, '2024-02-02 09:20:00');
INSERT INTO public.products VALUES (6, 2, 'Celana Chino Slim Fit', 'Celana chino slim fit warna khaki', 215000.00, 45, '2024-02-05 13:10:00');
INSERT INTO public.products VALUES (7, 2, 'Sepatu Sneakers Pria', 'Sepatu sneakers casual bahan kanvas', 329000.00, 30, '2024-02-10 15:00:00');
INSERT INTO public.products VALUES (8, 3, 'Dress Wanita Motif Bunga', 'Dress casual motif bunga bahan katun rayon', 199000.00, 55, '2024-02-14 10:30:00');
INSERT INTO public.products VALUES (9, 3, 'Tas Selempang Wanita', 'Tas selempang kulit sintetis ukuran medium', 159000.00, 70, '2024-02-18 14:20:00');
INSERT INTO public.products VALUES (10, 4, 'Blender Portable', 'Blender mini portable rechargeable', 210000.00, 25, '2024-03-01 08:00:00');
INSERT INTO public.products VALUES (11, 4, 'Rice Cooker 1.8L', 'Rice cooker kapasitas 1.8 liter anti lengket', 385000.00, 18, '2024-03-04 09:30:00');
INSERT INTO public.products VALUES (12, 5, 'Matras Yoga Anti Slip', 'Matras yoga tebal 10mm anti slip', 95000.00, 50, '2024-03-10 11:00:00');
INSERT INTO public.products VALUES (13, 5, 'Dumbbell Set 5kg', 'Set dumbbell besi lapis karet berat 5kg per unit', 275000.00, 22, '2024-03-15 16:40:00');
INSERT INTO public.products VALUES (14, 6, 'Novel Laskar Pelangi', 'Novel best seller karya Andrea Hirata', 78000.00, 200, '2024-03-20 10:10:00');
INSERT INTO public.products VALUES (15, 6, 'Buku Tulis Sinar Dunia (1 Lusin)', 'Buku tulis isi 38 lembar, satu lusin', 45000.00, 150, '2024-03-22 09:00:00');
INSERT INTO public.products VALUES (16, 7, 'Kopi Bubuk Gayo 250gr', 'Kopi bubuk arabika asal Gayo kemasan 250gr', 65000.00, 90, '2024-04-01 08:30:00');
INSERT INTO public.products VALUES (17, 7, 'Keripik Singkong Pedas', 'Keripik singkong renyah rasa pedas manis', 18000.00, 250, '2024-04-03 10:00:00');


--
-- TOC entry 5054 (class 0 OID 17224)
-- Dependencies: 228
-- Data for Name: order_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.order_items VALUES (1, 1, 2, 1, 450000.00);
INSERT INTO public.order_items VALUES (2, 1, 3, 1, 175000.00);
INSERT INTO public.order_items VALUES (3, 2, 8, 1, 199000.00);
INSERT INTO public.order_items VALUES (4, 3, 5, 2, 189000.00);
INSERT INTO public.order_items VALUES (5, 3, 6, 1, 215000.00);
INSERT INTO public.order_items VALUES (6, 4, 11, 1, 385000.00);
INSERT INTO public.order_items VALUES (7, 5, 15, 2, 45000.00);
INSERT INTO public.order_items VALUES (8, 5, 17, 3, 18000.00);
INSERT INTO public.order_items VALUES (9, 6, 7, 1, 329000.00);
INSERT INTO public.order_items VALUES (10, 6, 4, 2, 35000.00);
INSERT INTO public.order_items VALUES (11, 7, 10, 1, 210000.00);
INSERT INTO public.order_items VALUES (12, 7, 12, 2, 95000.00);
INSERT INTO public.order_items VALUES (13, 8, 9, 3, 159000.00);
INSERT INTO public.order_items VALUES (14, 9, 2, 1, 450000.00);
INSERT INTO public.order_items VALUES (15, 9, 4, 2, 35000.00);
INSERT INTO public.order_items VALUES (16, 9, 16, 1, 65000.00);
INSERT INTO public.order_items VALUES (17, 10, 14, 2, 78000.00);
INSERT INTO public.order_items VALUES (18, 10, 17, 5, 18000.00);
INSERT INTO public.order_items VALUES (19, 11, 13, 1, 275000.00);
INSERT INTO public.order_items VALUES (20, 12, 6, 1, 215000.00);


--
-- TOC entry 5061 (class 0 OID 0)
-- Dependencies: 221
-- Name: category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.category_id_seq', 7, true);


--
-- TOC entry 5062 (class 0 OID 0)
-- Dependencies: 227
-- Name: order_items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.order_items_id_seq', 20, true);


--
-- TOC entry 5063 (class 0 OID 0)
-- Dependencies: 225
-- Name: orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.orders_id_seq', 13, true);


--
-- TOC entry 5064 (class 0 OID 0)
-- Dependencies: 223
-- Name: products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.products_id_seq', 17, true);


--
-- TOC entry 5065 (class 0 OID 0)
-- Dependencies: 219
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 10, true);


-- Completed on 2026-08-29 03:08:18

--
-- PostgreSQL database dump complete
--

\unrestrict bQJbnJ7VKG2umhXET9TGqc4X28AA7KIA0pTQ2I0rrdnZpq1MebMqFndTqFfjV8L

