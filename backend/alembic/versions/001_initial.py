"""Initial migration

Revision ID: 001_initial
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('username', sa.String(length=255), nullable=True),
        sa.Column('hashed_password', sa.String(length=255), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('is_admin', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    
    # Create channels table
    op.create_table(
        'channels',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('channel_username', sa.String(length=255), nullable=False),
        sa.Column('channel_name', sa.String(length=255), nullable=False),
        sa.Column('channel_avatar_url', sa.String(length=512), nullable=True),
        sa.Column('subscribers_count', sa.Integer(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('parse_mode', sa.String(length=50), nullable=True),
        sa.Column('last_parsed_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_channels_channel_username'), 'channels', ['channel_username'], unique=True)
    op.create_index(op.f('ix_channels_id'), 'channels', ['id'], unique=False)
    
    # Create posts table
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('post_id', sa.String(length=255), nullable=False),
        sa.Column('channel_id', sa.Integer(), nullable=False),
        sa.Column('text', sa.Text(), nullable=True),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('author', sa.String(length=255), nullable=True),
        sa.Column('views', sa.Integer(), nullable=True),
        sa.Column('likes', sa.Integer(), nullable=True),
        sa.Column('engagement_rate', sa.Float(), nullable=True),
        sa.Column('content_type', sa.String(length=50), nullable=False),
        sa.Column('media_urls', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('hashtags', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('mentions', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('links', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('parsed_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['channel_id'], ['channels.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_posts_channel_id'), 'posts', ['channel_id'], unique=False)
    op.create_index(op.f('ix_posts_content_type'), 'posts', ['content_type'], unique=False)
    op.create_index(op.f('ix_posts_date'), 'posts', ['date'], unique=False)
    op.create_index(op.f('ix_posts_id'), 'posts', ['id'], unique=False)
    op.create_index('idx_post_date_channel', 'posts', ['date', 'channel_id'], unique=False)


def downgrade() -> None:
    op.drop_index('idx_post_date_channel', table_name='posts')
    op.drop_table('posts')
    op.drop_index(op.f('ix_channels_id'), table_name='channels')
    op.drop_index(op.f('ix_channels_channel_username'), table_name='channels')
    op.drop_table('channels')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')

