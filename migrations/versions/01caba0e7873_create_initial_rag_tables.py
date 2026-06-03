"""create initial rag tables

Revision ID: 01caba0e7873
Revises: 
Create Date: 2026-06-01 17:18:20.734006

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '01caba0e7873'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    existing_tables = set(sa.inspect(op.get_bind()).get_table_names())

    if "documents" not in existing_tables:
        op.create_table(
            "documents",
            sa.Column("id", sa.String(length=64), nullable=False),
            sa.Column("filename", sa.String(length=255), nullable=False),
            sa.Column("source_path", sa.String(length=500), nullable=True),
            sa.Column("processed_path", sa.String(length=500), nullable=True),
            sa.Column("content_type", sa.String(length=100), nullable=True),
            sa.Column("status", sa.String(length=32), nullable=False),
            sa.Column("chunk_count", sa.Integer(), nullable=False),
            sa.Column("error_message", sa.Text(), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.Column("updated_at", sa.DateTime(), nullable=False),
            sa.PrimaryKeyConstraint("id"),
        )

    if "chunks" not in existing_tables:
        op.create_table(
            "chunks",
            sa.Column("id", sa.String(length=96), nullable=False),
            sa.Column("document_id", sa.String(length=64), nullable=False),
            sa.Column("source", sa.String(length=255), nullable=False),
            sa.Column("page", sa.Integer(), nullable=True),
            sa.Column("section", sa.String(length=255), nullable=True),
            sa.Column("position", sa.Integer(), nullable=False),
            sa.Column("content", sa.Text(), nullable=False),
            sa.Column("embedding", sa.JSON(), nullable=True),
            sa.Column("score", sa.Float(), nullable=True),
            sa.Column("embedding_model", sa.String(length=255), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.ForeignKeyConstraint(["document_id"], ["documents.id"]),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(
            "ix_chunks_document_id",
            "chunks",
            ["document_id"],
            unique=False,
        )

    if "qa_logs" not in existing_tables:
        op.create_table(
            "qa_logs",
            sa.Column("id", sa.String(length=64), nullable=False),
            sa.Column("question", sa.Text(), nullable=False),
            sa.Column("answer", sa.Text(), nullable=False),
            sa.Column("sources", sa.JSON(), nullable=False),
            sa.Column("top_k", sa.Integer(), nullable=False),
            sa.Column("llm_provider", sa.String(length=100), nullable=True),
            sa.Column("llm_model", sa.String(length=255), nullable=True),
            sa.Column("latency_ms", sa.Integer(), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.PrimaryKeyConstraint("id"),
        )


def downgrade() -> None:
    """Downgrade schema."""
    existing_tables = set(sa.inspect(op.get_bind()).get_table_names())

    if "qa_logs" in existing_tables:
        op.drop_table("qa_logs")

    if "chunks" in existing_tables:
        op.drop_index("ix_chunks_document_id", table_name="chunks")
        op.drop_table("chunks")

    if "documents" in existing_tables:
        op.drop_table("documents")
