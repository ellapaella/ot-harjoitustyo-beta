import os
import pytest
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load test environment variables
load_dotenv(".env.test")

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
os.environ["DATABASE_URL"] = TEST_DATABASE_URL

from db import storage


@pytest.fixture(scope="function", autouse=True)
def clean_database():
    """
    Reset test database before each test.

    Drops all existing data while preserving schema.
    """
    engine = create_engine(TEST_DATABASE_URL)

    with engine.connect() as conn:
        # Order matters because of foreign keys
        conn.execute(text("TRUNCATE TABLE Plots RESTART IDENTITY CASCADE;"))
        conn.execute(text("TRUNCATE TABLE Users RESTART IDENTITY CASCADE;"))
        conn.commit()

    yield

def test_storage_adds_user():
    pass