"""rename category table to categories

Revision ID: a1b2c3d4e5f6
Revises: fcc7eff89951
Create Date: 2026-09-09 00:00:00.000000

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = 'fcc7eff89951'
branch_labels = None
depends_on = None


def upgrade():
    # Rename the table. The existing foreign key from products.category_id
    # keeps pointing at the same table automatically, and Postgres keeps the
    # sequence/primary-key working under their old names.
    op.rename_table('category', 'categories')


def downgrade():
    op.rename_table('categories', 'category')
