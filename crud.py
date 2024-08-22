from typing import List, Optional
from sqlalchemy.orm import Session
import models, schemas

def create_department(db: Session, department: schemas.DepartmentCreate) -> models.Department:
    """
    Create a new department in the database.

    Args:
        db (Session): The database session.
        department (schemas.DepartmentCreate): The department data to create.

    Returns:
        models.Department: The created department.
    """
    db_department = models.Department(**department.dict())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department

def get_employees(
    db: Session,
    department_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 10
) -> List[models.Employee]:
    """
    Retrieve a list of employees from the database with optional filtering by department.

    Args:
        db (Session): The database session.
        department_id (Optional[int]): Optional department ID to filter employees.
        skip (int): Number of employees to skip (for pagination).
        limit (int): Maximum number of employees to return.

    Returns:
        List[models.Employee]: A list of employees.
    """
    query = db.query(models.Employee)
    if department_id:
        query = query.filter(models.Employee.department_id == department_id)
    return query.offset(skip).limit(limit).all()

def create_employee(db: Session, employee: schemas.EmployeeCreate) -> models.Employee:
    """
    Create a new employee in the database.

    Args:
        db (Session): The database session.
        employee (schemas.EmployeeCreate): The employee data to create.

    Returns:
        models.Employee: The created employee.
    """
    db_employee = models.Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def get_departments(db: Session, skip: int = 0, limit: int = 10) -> List[models.Department]:
    """
    Retrieve a list of departments from the database with pagination.

    Args:
        db (Session): The database session.
        skip (int): Number of departments to skip (for pagination).
        limit (int): Maximum number of departments to return.

    Returns:
        List[models.Department]: A list of departments.
    """
    return db.query(models.Department).offset(skip).limit(limit).all()
