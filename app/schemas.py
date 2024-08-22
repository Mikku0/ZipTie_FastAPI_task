from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

class EmployeeBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    email: EmailStr
    department_id: Optional[int] = None

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: int

    class Config:
        orm_mode = True

class DepartmentBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    location: str = Field(min_length=1, max_length=100)

class DepartmentCreate(DepartmentBase):
    pass

class Department(DepartmentBase):
    id: int
    employees: List[Employee] = []

    class Config:
        orm_mode = True
