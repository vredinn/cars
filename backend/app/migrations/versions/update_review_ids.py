"""update review ids to use uuid

Revision ID: update_review_ids
Revises: 954bdfb4955a
Create Date: 2024-03-19 10:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision: str = 'update_review_ids'
down_revision: Union[str, None] = '954bdfb4955a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema to use UUIDs."""
    # Add new UUID columns
    op.add_column('reviews', sa.Column('user_uuid', UUID(as_uuid=True), nullable=True))
    op.add_column('reviews', sa.Column('seller_uuid', UUID(as_uuid=True), nullable=True))
    op.add_column('reviews', sa.Column('deal_uuid', UUID(as_uuid=True), nullable=True))
    
    # Update the new columns with UUID values from related tables
    op.execute("""
        UPDATE reviews r
        SET user_uuid = u.uuid
        FROM users u
        WHERE r.user_id = u.id
    """)
    
    op.execute("""
        UPDATE reviews r
        SET seller_uuid = u.uuid
        FROM users u
        WHERE r.seller_id = u.id
    """)
    
    op.execute("""
        UPDATE reviews r
        SET deal_uuid = d.uuid
        FROM deals d
        WHERE r.deal_id = d.id
    """)
    
    # Make the new columns not nullable
    op.alter_column('reviews', 'user_uuid', nullable=False)
    op.alter_column('reviews', 'seller_uuid', nullable=False)
    op.alter_column('reviews', 'deal_uuid', nullable=False)
    
    # Add foreign key constraints
    op.create_foreign_key('fk_reviews_user_uuid', 'reviews', 'users', ['user_uuid'], ['uuid'], ondelete='CASCADE')
    op.create_foreign_key('fk_reviews_seller_uuid', 'reviews', 'users', ['seller_uuid'], ['uuid'], ondelete='CASCADE')
    op.create_foreign_key('fk_reviews_deal_uuid', 'reviews', 'deals', ['deal_uuid'], ['uuid'], ondelete='CASCADE')
    
    # Drop old columns and constraints
    op.drop_constraint('reviews_user_id_fkey', 'reviews', type_='foreignkey')
    op.drop_constraint('reviews_seller_id_fkey', 'reviews', type_='foreignkey')
    op.drop_constraint('reviews_deal_id_fkey', 'reviews', type_='foreignkey')
    op.drop_constraint('uq_deal_review', 'reviews', type_='unique')
    
    op.create_unique_constraint('uq_deal_uuid_review', 'reviews', ['deal_uuid'])
    
    op.drop_column('reviews', 'user_id')
    op.drop_column('reviews', 'seller_id')
    op.drop_column('reviews', 'deal_id')

def downgrade() -> None:
    """Downgrade schema back to using integer IDs."""
    # Add back the old columns
    op.add_column('reviews', sa.Column('user_id', sa.Integer(), nullable=True))
    op.add_column('reviews', sa.Column('seller_id', sa.Integer(), nullable=True))
    op.add_column('reviews', sa.Column('deal_id', sa.Integer(), nullable=True))
    
    # Update the old columns with ID values from related tables
    op.execute("""
        UPDATE reviews r
        SET user_id = u.id
        FROM users u
        WHERE r.user_uuid = u.uuid
    """)
    
    op.execute("""
        UPDATE reviews r
        SET seller_id = u.id
        FROM users u
        WHERE r.seller_uuid = u.uuid
    """)
    
    op.execute("""
        UPDATE reviews r
        SET deal_id = d.id
        FROM deals d
        WHERE r.deal_uuid = d.uuid
    """)
    
    # Make the old columns not nullable
    op.alter_column('reviews', 'user_id', nullable=False)
    op.alter_column('reviews', 'seller_id', nullable=False)
    op.alter_column('reviews', 'deal_id', nullable=False)
    
    # Add back the old constraints
    op.create_foreign_key('reviews_user_id_fkey', 'reviews', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('reviews_seller_id_fkey', 'reviews', 'users', ['seller_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('reviews_deal_id_fkey', 'reviews', 'deals', ['deal_id'], ['id'], ondelete='CASCADE')
    op.create_unique_constraint('uq_deal_review', 'reviews', ['deal_id'])
    
    # Drop new columns and constraints
    op.drop_constraint('fk_reviews_user_uuid', 'reviews', type_='foreignkey')
    op.drop_constraint('fk_reviews_seller_uuid', 'reviews', type_='foreignkey')
    op.drop_constraint('fk_reviews_deal_uuid', 'reviews', type_='foreignkey')
    op.drop_constraint('uq_deal_uuid_review', 'reviews', type_='unique')
    
    op.drop_column('reviews', 'user_uuid')
    op.drop_column('reviews', 'seller_uuid')
    op.drop_column('reviews', 'deal_uuid') 