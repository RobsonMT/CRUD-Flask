"""removing api_key column

Revision ID: 861117808146
Revises: 933a2f4677a8
Create Date: 2022-04-21 09:24:00.414080

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "861117808146"
down_revision = "933a2f4677a8"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "api_key")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users",
        sa.Column(
            "api_key", sa.VARCHAR(length=511), autoincrement=False, nullable=False
        ),
    )
    # ### end Alembic commands ###