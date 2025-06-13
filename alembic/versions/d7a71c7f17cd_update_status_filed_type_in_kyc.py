"""Update status filed type in KYC

Revision ID: d7a71c7f17cd
Revises: 0e71cec05498
Create Date: 2025-06-13 11:07:32.933174

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM


# revision identifiers, used by Alembic.
revision: str = 'd7a71c7f17cd'
down_revision: Union[str, None] = '0e71cec05498'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

new_kycstatus_enum = ENUM('Draft', 'Pending', 'Approved', 'Rejected', name='kycstatus')
old_kycstatus_enum = ENUM('draft', 'pending', 'approved', 'rejected', name='kycstatus')


def upgrade() -> None:
    """Upgrade schema."""
     # Rename the old enum type
    op.execute("ALTER TYPE kycstatus RENAME TO kycstatus_old")
     # Create the new enum type
    new_kycstatus_enum.create(op.get_bind(), checkfirst=True)

    # Temporarily change the column type to TEXT
    op.execute("ALTER TABLE kyc ALTER COLUMN status TYPE TEXT USING status::text")

    # Update the column to use the new enum type
    op.execute("ALTER TABLE kyc ALTER COLUMN status TYPE kycstatus USING status::kycstatus")

    # Drop the old enum type
    op.execute("DROP TYPE kycstatus_old")

def downgrade() -> None:
    # Recreate the old enum type
    old_kycstatus_enum.create(op.get_bind(), checkfirst=True)

   # Update the column to use the old enum type
    op.execute("ALTER TABLE kyc ALTER COLUMN status TYPE kycstatus USING status::kycstatus")

    # Drop the new enum type
    op.execute("DROP TYPE kycstatus")
