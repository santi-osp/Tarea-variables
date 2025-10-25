"""Initial migration

Revision ID: 001_initial
Revises:
Create Date: 2025-01-16 10:00:00.000000

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create categorias table
    op.create_table(
        "categorias",
        sa.Column("id_categoria", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("nombre", sa.String(length=100), nullable=False),
        sa.Column("descripcion", sa.Text(), nullable=True),
        sa.Column("activa", sa.Boolean(), nullable=True),
        sa.Column(
            "fecha_creacion",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("fecha_edicion", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id_categoria"),
    )
    op.create_index(
        op.f("ix_categorias_id_categoria"), "categorias", ["id_categoria"], unique=False
    )

    # Create tbl_usuarios table
    op.create_table(
        "tbl_usuarios",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("nombre", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("telefono", sa.String(length=20), nullable=True),
        sa.Column("activo", sa.Boolean(), nullable=True),
        sa.Column(
            "fecha_creacion",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("fecha_edicion", sa.DateTime(timezone=True), nullable=True),
        sa.Column("nombre_usuario", sa.String(length=50), nullable=True),
        sa.Column("contrasena_hash", sa.String(length=255), nullable=True),
        sa.Column("es_admin", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_tbl_usuarios_id"), "tbl_usuarios", ["id"], unique=False)
    op.create_index(
        op.f("ix_usuarios_nombre_usuario"),
        "tbl_usuarios",
        ["nombre_usuario"],
        unique=True,
    )

    # Create productos table
    op.create_table(
        "productos",
        sa.Column("id_producto", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("nombre", sa.String(length=200), nullable=False),
        sa.Column("descripcion", sa.Text(), nullable=True),
        sa.Column("precio", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("stock", sa.Integer(), nullable=True),
        sa.Column(
            "fecha_creacion",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("fecha_edicion", sa.DateTime(timezone=True), nullable=True),
        sa.Column("categoria_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("usuario_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("id_usuario_crea", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("id_usuario_edita", postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["categoria_id"],
            ["categorias.id_categoria"],
        ),
        sa.ForeignKeyConstraint(
            ["id_usuario_crea"],
            ["tbl_usuarios.id"],
        ),
        sa.ForeignKeyConstraint(
            ["id_usuario_edita"],
            ["tbl_usuarios.id"],
        ),
        sa.ForeignKeyConstraint(
            ["usuario_id"],
            ["tbl_usuarios.id"],
        ),
        sa.PrimaryKeyConstraint("id_producto"),
    )
    op.create_index(
        op.f("ix_productos_id_producto"), "productos", ["id_producto"], unique=False
    )


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_index(op.f("ix_productos_id_producto"), table_name="productos")
    op.drop_table("productos")
    op.drop_index(op.f("ix_usuarios_nombre_usuario"), table_name="tbl_usuarios")
    op.drop_index(op.f("ix_tbl_usuarios_id"), table_name="tbl_usuarios")
    op.drop_table("tbl_usuarios")
    op.drop_index(op.f("ix_categorias_id_categoria"), table_name="categorias")
    op.drop_table("categorias")

