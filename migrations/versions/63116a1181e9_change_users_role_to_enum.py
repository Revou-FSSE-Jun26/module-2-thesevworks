"""change users.role from String to Enum(buyer, admin)

Revision ID: 63116a1181e9
Revises: a1b2c3d4e5f6
Create Date: 2026-10-30

NOTE: This migration is intentionally scoped to ONLY convert users.role
from VARCHAR to a Postgres ENUM type (user_role). It deliberately does NOT
touch any other column, constraint, or foreign key. Raw SQL is used because
batch_alter_table does not CREATE TYPE nor add the required USING clause for
a VARCHAR -> ENUM conversion in PostgreSQL.
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "63116a1181e9"
down_revision = "a1b2c3d4e5f6"
branch_labels = None
depends_on = None


def upgrade():
    # 1. Drop the existing default so the column can be retyped cleanly.
    op.execute("ALTER TABLE users ALTER COLUMN role DROP DEFAULT")
    # 2. Create the enum type if it does not already exist (idempotent).
    op.execute(
        "DO $$ BEGIN "
        "IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_role') THEN "
        "CREATE TYPE user_role AS ENUM ('buyer', 'admin'); "
        "END IF; END $$;"
    )
    # 3. Convert the column, casting existing text values into the enum.
    op.execute(
        "ALTER TABLE users ALTER COLUMN role TYPE user_role "
        "USING role::text::user_role"
    )
    # 4. Restore the default as the enum value.
    op.execute("ALTER TABLE users ALTER COLUMN role SET DEFAULT 'buyer'::user_role")


def downgrade():
    # Reverse: enum -> VARCHAR(25), then drop the enum type.
    op.execute("ALTER TABLE users ALTER COLUMN role DROP DEFAULT")
    op.execute("ALTER TABLE users ALTER COLUMN role TYPE VARCHAR(25) USING role::text")
    op.execute("ALTER TABLE users ALTER COLUMN role SET DEFAULT 'buyer'")
    op.execute("DROP TYPE IF EXISTS user_role")
