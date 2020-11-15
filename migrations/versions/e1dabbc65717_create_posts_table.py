"""create posts table

Revision ID: e1dabbc65717
Revises:
Create Date: 2020-11-11 23:37:30.523807

"""
import sqlalchemy
from alembic import op

# revision identifiers, used by Alembic.
revision = "e1dabbc65717"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "posts",
        sqlalchemy.Column("post_id", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("title", sqlalchemy.String, nullable=False),
        sqlalchemy.Column("subtitle", sqlalchemy.String, nullable=False),
        sqlalchemy.Column("author", sqlalchemy.String, nullable=False),
        sqlalchemy.Column("date", sqlalchemy.DateTime, nullable=False),
        sqlalchemy.Column("content", sqlalchemy.Text, nullable=False),
        sqlalchemy.Column("completed", sqlalchemy.Boolean, nullable=False),
    )

    op.create_table(
        "post_tags",
        sqlalchemy.Column(
            "post_id",
            sqlalchemy.Integer,
            sqlalchemy.ForeignKey("posts.post_id"),
            primary_key=True,
        ),
        sqlalchemy.Column(
            "tag_id",
            sqlalchemy.Integer,
            sqlalchemy.ForeignKey("tags.tag_id"),
            primary_key=True,
        ),
    )

    op.create_table(
        "tags",
        sqlalchemy.Column("tag_id", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("name", sqlalchemy.String, nullable=False),
        sqlalchemy.Column("description", sqlalchemy.String, nullable=False),
    )


def downgrade():
    op.drop_table("posts")
    op.drop_table("post_tags")
    op.drop_table("tags")
