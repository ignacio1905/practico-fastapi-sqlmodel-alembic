"""migracion inicial: tablas autores y libros

Revision ID: a1b2c3d4e5f6
Revises:
Create Date: 2026-10-27 17:30:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "autores",
        sa.Column("nombre", sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
        sa.Column("nacionalidad", sqlmodel.sql.sqltypes.AutoString(length=50), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_autores_nombre"), "autores", ["nombre"], unique=False)

    op.create_table(
        "libros",
        sa.Column("titulo", sqlmodel.sql.sqltypes.AutoString(length=200), nullable=False),
        sa.Column("anio", sa.Integer(), nullable=True),
        sa.Column("genero", sqlmodel.sql.sqltypes.AutoString(length=50), nullable=True),
        sa.Column("leido", sa.Boolean(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("autor_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["autor_id"], ["autores.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_libros_titulo"), "libros", ["titulo"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_libros_titulo"), table_name="libros")
    op.drop_table("libros")
    op.drop_index(op.f("ix_autores_nombre"), table_name="autores")
    op.drop_table("autores")
