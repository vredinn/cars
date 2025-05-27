"""add uuid to messages

Revision ID: 50a23f0767cd
Revises: 5951816748dc
Create Date: 2025-05-27 14:37:10.330724

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import UUID
import uuid


# revision identifiers, used by Alembic.
revision: str = '50a23f0767cd'
down_revision: Union[str, None] = '5951816748dc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # 1. Добавляем колонку nullable=True временно
    op.add_column('messages', sa.Column('uuid', UUID(as_uuid=True), nullable=True))

    # 2. Заполняем uuid значением uuid4 для уже существующих строк
    conn = op.get_bind()
    result = conn.execute(sa.text("SELECT id FROM messages"))
    rows = result.fetchall()

    for row in rows:
        conn.execute(
            sa.text("UPDATE messages SET uuid = :uuid WHERE id = :id"),
            {"uuid": str(uuid.uuid4()), "id": row.id}
        )

    # 3. Делаем колонку NOT NULL и добавляем уникальный индекс
    op.alter_column('messages', 'uuid', nullable=False)
    op.create_index(op.f('ix_messages_uuid'), 'messages', ['uuid'], unique=True)


def downgrade():
    op.drop_index(op.f('ix_messages_uuid'), table_name='messages')
    op.drop_column('messages', 'uuid')
