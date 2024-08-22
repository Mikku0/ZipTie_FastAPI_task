import pytest
from pydantic import ValidationError
from app.schemas import DepartmentCreate, EmployeeCreate

def test_valid_department_create():
    department = DepartmentCreate(name="HR", location="New York")
    assert department.name == "HR"
    assert department.location == "New York"

def test_invalid_department_create():
    with pytest.raises(ValidationError):
        DepartmentCreate(name="HR", location="")  # location is too short

def test_valid_employee_create():
    employee = EmployeeCreate(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        department_id=1
    )
    assert employee.first_name == "John"
    assert employee.email == "john.doe@example.com"

def test_invalid_employee_create():
    with pytest.raises(ValidationError):
        EmployeeCreate(
            first_name="John",
            last_name="Doe",
            email="not-an-email",  # Invalid email
            department_id=1
        )
