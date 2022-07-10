"""Initial setup

Revision ID: ff8f90a37f32
Revises: 
Create Date: 2022-07-10 09:46:38.181714

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = 'ff8f90a37f32'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(80), nullable=False, unique=True),
        sa.Column('password', sa.String(120), nullable=False, unique=True),
        sa.Column('email', sa.String(120), nullable=False, unique=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False,
                  default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), nullable=False,
                  default=datetime.utcnow),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'links',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('unique_id', sa.String(120), nullable=False, unique=True),
        sa.Column('original_url', sa.Text, nullable=False),
        sa.Column('visits_used', sa.Integer, nullable=False, default=0),
        sa.Column('visits_allowed', sa.Integer, nullable=False, default=1),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('is_available', sa.Boolean, nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False,
                  default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), nullable=False,
                  default=datetime.utcnow),
        sa.Column('comment', sa.Text),
        sa.PrimaryKeyConstraint('id'),
    )

    # Not implemented in SQLite3
    # op.create_foreign_key(
    #     'links_users_fk', 'links', 'users', ['user_id'], ['id']
    # )

    op.create_table(
        'clicks',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('ip_address', sa.String(80), nullable=False),
        sa.Column('link_id', sa.Integer, nullable=False),
        sa.Column('was_available', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False,
                  default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), nullable=False,
                  default=datetime.utcnow),
        sa.PrimaryKeyConstraint('id'),
    )

    # Not implemented in SQLite3
    # op.create_foreign_key(
    #     'clicks_links_fk', 'clicks', 'links', ['link_id'], ['id']
    # )


def downgrade():
    op.drop_table('users')
    op.drop_table('links')
    op.drop_table('clicks')
