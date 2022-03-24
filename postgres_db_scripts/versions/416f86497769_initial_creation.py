"""Initial creation

Revision ID: 416f86497769
Revises: 
Create Date: 2022-03-21 19:15:57.038170

"""
from sqlmodel import SQLModel

from poke.database_interface import engine


# revision identifiers, used by Alembic.
revision = '416f86497769'
down_revision = None
branch_labels = None
depends_on = None

import os
print(os.environ.get('DB_CONN'))


def upgrade():
    print(os.environ.get('DB_CONN'))
    from poke.poke_model import pokemon  # Import this here as it is needed by the create_all call below.
    SQLModel.metadata.create_all(engine)
    print('done')


def downgrade():
    from poke.poke_model import pokemon  # Import this here as it is needed by the drop_all call below.
    SQLModel.metadata.drop_all(engine)
