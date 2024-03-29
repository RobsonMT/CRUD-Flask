"""update password_hash to nullable=True

Revision ID: 9d3ebcf40af3
Revises: 861117808146
Create Date: 2022-05-10 19:27:20.560325

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "9d3ebcf40af3"
down_revision = "861117808146"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "users", "password_hash", existing_type=sa.VARCHAR(length=511), nullable=True
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "users", "password_hash", existing_type=sa.VARCHAR(length=511), nullable=False
    )
    # ### end Alembic commands ###
