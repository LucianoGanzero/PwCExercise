from datetime import date

from pydantic import BaseModel


class EmployeeSchema(BaseModel):
    """Schema for employee data."""

    id: int
    name: str
    department_id: int
    hire_date: date
    job_title: str
    status: str

    class Config:
        orm_mode = True

