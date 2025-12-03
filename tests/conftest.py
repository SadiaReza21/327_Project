import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)


import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.database import Base

from models.product import Product
from models.inventory import Inventory
from models.archived import Archived
from models.category import Category


TEST_DB_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DB_URL)
SessionTesting = sessionmaker(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(engine)
    session = SessionTesting()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)
