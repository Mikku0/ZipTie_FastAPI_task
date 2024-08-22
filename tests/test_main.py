import pytest
from fastapi.testclient import TestClient
from app.main import app, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
import os

# Create a testing database engine and session
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite:///./tests/test_employees.db")
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="session")
def setup_db():
    # Set up the database schema
    Base.metadata.create_all(bind=engine)
    yield
    # Teardown: drop the schema after tests are done
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(setup_db):
    # Create a new session for each test
    db = TestingSessionLocal()
    yield db
    db.close()

def test_create_department(db_session):
    response = client.post("/departments/", json={"name": "HR", "location": "New York"})
    assert response.status_code == 200
    assert response.json()["name"] == "HR"
    assert response.json()["location"] == "New York"

def test_create_employee(db_session):
    department_response = client.post("/departments/", json={"name": "Engineering", "location": "San Francisco"})
    department_id = department_response.json()["id"]
    response = client.post("/employees/", json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "department_id": department_id
    })
    assert response.status_code == 200
    assert response.json()["first_name"] == "John"
    assert response.json()["last_name"] == "Doe"
    assert response.json()["email"] == "john.doe@example.com"

def test_read_departments(db_session):
    client.post("/departments/", json={"name": "Marketing", "location": "Chicago"})
    response = client.get("/departments/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_read_employees(db_session):
    department_response = client.post("/departments/", json={"name": "Finance", "location": "Boston"})
    department_id = department_response.json()["id"]
    client.post("/employees/", json={
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice.smith@example.com",
        "department_id": department_id
    })
    response = client.get("/employees/", params={"department_id": department_id})
    assert response.status_code == 200
    assert len(response.json()) > 0
