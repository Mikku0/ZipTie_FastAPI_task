import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from app.crud import create_department, get_employees, create_employee, get_departments
from app.models import Department, Employee
from app.schemas import DepartmentCreate, EmployeeCreate
from test_database import engine, Base

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite:///./tests/test_employees.db")
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def db():
    # Set up the test database
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_create_department(db: Session):
    department_data = DepartmentCreate(name="HR", location="New York")
    department = create_department(db, department_data)
    assert department.name == "HR"
    assert department.location == "New York"

def test_get_departments(db: Session):
    department_data = DepartmentCreate(name="Finance", location="Boston")
    create_department(db, department_data)
    departments = get_departments(db)
    assert len(departments) > 0

def test_create_employee(db: Session):
    department_data = DepartmentCreate(name="Engineering", location="San Francisco")
    department = create_department(db, department_data)
    employee_data = EmployeeCreate(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        department_id=department.id
    )
    employee = create_employee(db, employee_data)
    assert employee.first_name == "John"
    assert employee.email == "john.doe@example.com"

def test_get_employees(db: Session):
    department_data = DepartmentCreate(name="Marketing", location="Chicago")
    department = create_department(db, department_data)
    employee_data = EmployeeCreate(
        first_name="Jane",
        last_name="Doe",
        email="jane.doe@example.com",
        department_id=department.id
    )
    create_employee(db, employee_data)
    employees = get_employees(db, department_id=department.id)
    assert len(employees) > 0
