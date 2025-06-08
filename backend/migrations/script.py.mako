from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector

"""Initial migration for MemoryEntry table"""

# revision identifiers, used by Alembic.
revision = 'initial_migration'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'memory_entries',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False, index=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('embedding', Vector(1536), nullable=True),
        sa.Column('entry_metadata', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_memory_entries_user_id'), 'memory_entries', ['user_id'], unique=False)
    op.execute(sa.text("CREATE EXTENSION IF NOT EXISTS vector"))

def downgrade():
    op.drop_index(op.f('ix_memory_entries_user_id'), table_name='memory_entries')
    op.drop_table('memory_entries')
