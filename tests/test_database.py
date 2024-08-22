import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, engine

@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_database_connection():
    try:
        connection = engine.connect()
        assert connection is not None
    except Exception as e:
        pytest.fail(f"Database connection failed: {e}")

def test_base_declarative():
    assert Base is not None
