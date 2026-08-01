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

![Schema Diagram] (C:\Users\Lenovo\Documents\Lightshot\Checkpoint Revoshop\ERD.png)

## Notes

The role column in the users table has been intentionally omitted at this stage — it will be introduced via a live schema migration in Checkpoint 2.
