"""Update KYCStatus enum values to lowercase

Revision ID: c15aeecccd24
Revises: d7a71c7f17cd
Create Date: 2025-06-13 11:39:05.129396

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM


# revision identifiers, used by Alembic.
revision: str = 'c15aeecccd24'
down_revision: Union[str, None] = 'd7a71c7f17cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Define the new and old ENUM types
new_kycstatus_enum = ENUM('draft', 'pending', 'approved', 'rejected', name='kycstatus')
old_kycstatus_enum = ENUM('Draft', 'Pending', 'Approved', 'Rejected', name='kycstatus')

def upgrade():
    # Rename the old enum type
    op.execute("ALTER TYPE kycstatus RENAME TO kycstatus_old")

    # Create the new enum type
    new_kycstatus_enum.create(op.get_bind(), checkfirst=True)

    # Temporarily change the column type to TEXT
    op.execute("ALTER TABLE kyc ALTER COLUMN status TYPE TEXT USING status::text")

    # Update the values in the column to match the new enum
    op.execute("UPDATE kyc SET status = LOWER(status)")

    # Change the column type to the new enum
    op.execute("ALTER TABLE kyc ALTER COLUMN status TYPE kycstatus USING status::kycstatus")

    # Drop the old enum type
    op.execute("DROP TYPE kycstatus_old")


def downgrade():
    # Recreate the old enum type
    old_kycstatus_enum.create(op.get_bind(), checkfirst=True)

    # Temporarily change the column type to TEXT
    op.execute("ALTER TABLE kyc ALTER COLUMN status TYPE TEXT USING status::text")

    # Update the values in the column to match the old enum
    op.execute("""
        UPDATE kyc
        SET status = CASE
            WHEN status = 'draft' THEN 'Draft'
            WHEN status = 'pending' THEN 'Pending'
            WHEN status = 'approved' THEN 'Approved'
            WHEN status = 'rejected' THEN 'Rejected'
        END
    """)

    # Change the column type to the old enum
    op.execute("ALTER TABLE kyc ALTER COLUMN status TYPE kycstatus USING status::kycstatus")

    # Drop the new enum type
    op.execute("DROP TYPE kycstatus")
