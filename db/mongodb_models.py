from pymongo import ASCENDING
from .db import client  # Import your initialized client

DB = client['skeets']


def setup_indexes():
    """Defines and creates all necessary indexes."""
    users_collection = DB['users']

    # Define the unique key (index) here
    users_collection.create_index(
        [('email', ASCENDING)],
        unique=True
    )

