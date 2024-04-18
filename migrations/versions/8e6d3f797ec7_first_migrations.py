"""first migrations

Revision ID: 8e6d3f797ec7
Revises: 19bd344e6870
Create Date: 2024-04-18 17:12:52.167383

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8e6d3f797ec7'
down_revision: Union[str, None] = '19bd344e6870'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
