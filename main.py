from fastapi import FastAPI, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
import schemas, crud
from database import SessionLocal

app = FastAPI()

def get_db():
    """
    Provides a database session for dependency injection.

    Yields:
        Session: A SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/departments/", response_model=List[schemas.Department])
def read_departments(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
) -> List[schemas.Department]:
    """
    Retrieve a list of departments with pagination.

    Args:
        skip (int): Number of departments to skip (for pagination).
        limit (int): Maximum number of departments to return.
        db (Session): The database session.

    Returns:
        List[schemas.Department]: A list of departments.
    """
    departments = crud.get_departments(db, skip=skip, limit=limit)
    return departments

@app.post("/departments/", response_model=schemas.Department)
def create_department(
    department: schemas.DepartmentCreate,
    db: Session = Depends(get_db)
) -> schemas.Department:
    """
    Create a new department.

    Args:
        department (schemas.DepartmentCreate): The department data to create.
        db (Session): The database session.

    Returns:
        schemas.Department: The created department.
    """
    return crud.create_department(db=db, department=department)

@app.post("/employees/", response_model=schemas.Employee)
def create_employee(
    employee: schemas.EmployeeCreate,
    db: Session = Depends(get_db)
) -> schemas.Employee:
    """
    Create a new employee.

    Args:
        employee (schemas.EmployeeCreate): The employee data to create.
        db (Session): The database session.

    Returns:
        schemas.Employee: The created employee.
    """
    return crud.create_employee(db=db, employee=employee)

@app.get("/employees/", response_model=List[schemas.Employee])
def read_employees(
    department_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
) -> List[schemas.Employee]:
    """
    Retrieve a list of employees with optional filtering by department and pagination.

    Args:
        department_id (Optional[int]): Optional department ID to filter employees.
        skip (int): Number of employees to skip (for pagination).
        limit (int): Maximum number of employees to return.
        db (Session): The database session.

    Returns:
        List[schemas.Employee]: A list of employees.
    """
    employees = crud.get_employees(db, department_id=department_id, skip=skip, limit=limit)
    return employees
