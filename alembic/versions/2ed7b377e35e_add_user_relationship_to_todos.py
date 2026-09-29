"""add user relationship to todos

Revision ID: 2ed7b377e35e
Revises: 41584e912089
Create Date: 2026-09-29 12:17:52.132576

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2ed7b377e35e"
down_revision: Union[str, Sequence[str], None] = "41584e912089"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    with op.batch_alter_table("todos", schema=None) as batch_op:

        batch_op.add_column(
            sa.Column(
                "user_id",
                sa.Integer(),
                nullable=False
            )
        )

        batch_op.create_foreign_key(
            "fk_todos_user_id_users",
            "users",
            ["user_id"],
            ["id"]
        )


def downgrade() -> None:
    """Downgrade schema."""

    with op.batch_alter_table("todos", schema=None) as batch_op:

        batch_op.drop_constraint(
            "fk_todos_user_id_users",
            type_="foreignkey"
        )

        batch_op.drop_column("user_id")