[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/wGq_UtnU)
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

2. Create the database:
   ```bash
   \CREATE DATABASE revoshop_db
   ```
3. Run the schema :
   ```bash
   psql -U postgres -d revoshop_db -f schema.sql
   ```
4. Insert Sample data :
   ```bash
   psql -U postgres -d revoshop_db -f seed.sql
   ```
5. Run sample queries for verification :
   ```bash
   psql -U postgres -d revoshop_db -f queries.sql
   ```

# ERD

See the relationship diagram between tables in erd.png (screenshot from pgAdmin/dbeaver diagram).

Relationship summary:

- users (1) — (N) orders

- categories (1) — (N) products

- orders (1) — (N) order_items

- products (1) — (N) order_items

## Notes

The role column in the users table has been intentionally omitted at this stage — it will be introduced via a live schema migration in Checkpoint 2.
