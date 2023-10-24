"""sink data

Revision ID: 4335b2f797a6
Revises: 57534efe22bb
Create Date: 2023-10-23 19:19:10.372220

"""
from alembic import op

from core.config import get_settings
from core.settings import EnvironmentTypes

# revision identifiers, used by Alembic.
revision = "4335b2f797a6"
down_revision = "4703e6ea0868"
branch_labels = None
depends_on = None


def upgrade() -> None:
    if get_settings().environment in (EnvironmentTypes.test, EnvironmentTypes.local):
        op.execute(
            """
            -- Insert 10 records into the "parlays" table with test data
            INSERT INTO parlays (token, user_token, event_token, amount, coefficient, created_at, status)
            VALUES
                ('11111111-1111-1111-1111-111111111111', 'user_token1', 'event_token1', 100, 2.0, '2023-10-24 10:00:00', 'PENDING'),
                ('22222222-2222-2222-2222-222222222222', 'user_token2', 'event_token2', 50, 1.5, '2023-10-24 10:15:00', 'WENT_IN'),
                ('33333333-3333-3333-3333-333333333333', 'user_token1', 'event_token2', 200, 3.0, '2023-10-24 10:30:00', 'LOST'),
                ('44444444-4444-4444-4444-444444444444', 'user_token3', 'event_token2', 75, 1.8, '2023-10-24 10:45:00', 'PENDING'),
                ('55555555-5555-5555-5555-555555555555', 'user_token2', 'event_token3', 300, 2.5, '2023-10-24 11:00:00', 'WENT_IN'),
                ('66666666-6666-6666-6666-666666666666', 'user_token3', 'event_token3', 150, 2.2, '2023-10-24 11:15:00', 'PENDING'),
                ('77777777-7777-7777-7777-777777777777', 'user_token1', 'event_token3', 50, 1.2, '2023-10-24 11:30:00', 'WENT_IN'),
                ('88888888-8888-8888-8888-888888888888', 'user_token2', 'event_token1', 100, 2.0, '2023-10-24 11:45:00', 'LOST'),
                ('99999999-9999-9999-9999-999999999999', 'user_token3', 'event_token1', 250, 1.7, '2023-10-24 12:00:00', 'PENDING'),
                ('00000000-0000-0000-0000-000000000000', 'user_token1', 'event_token2', 175, 2.3, '2023-10-24 12:15:00', 'WENT_IN');
            """
        )


def downgrade() -> None:
    if get_settings().environment in (EnvironmentTypes.test, EnvironmentTypes.local):
        op.execute(
            """
            TRUNCATE
                public.parlays
                CASCADE;
            """
        )
