"""add user roles

Revision ID: e95f07985da1
Revises: cc99648bd566
Create Date: 2026-01-24 19:58:53.426535

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision: str = 'e95f07985da1'
down_revision: Union[str, Sequence[str], None] = 'cc99648bd566'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None




def upgrade() -> None:
    # 1️⃣ Create enum type explicitly
    user_roles_enum = sa.Enum("user", "admin", name="user_roles")
    user_roles_enum.create(op.get_bind(), checkfirst=True)

    # 2️⃣ Add column using the enum
    op.add_column(
        "users",
        sa.Column(
            "role",
            user_roles_enum,
            nullable=False,
            server_default="user"
        )
    )


def downgrade() -> None:
    # 1️⃣ Drop column first
    op.drop_column("users", "role")

    # 2️⃣ Drop enum type
    sa.Enum("user", "admin", name="user_roles").drop(
        op.get_bind(), checkfirst=True
    )


