"""Module containing the schema definition for employee data."""

from datetime import date

from pydantic import BaseModel


class EmployeeSchema(BaseModel):
    """Schema for employee data."""

    id: int
    emp_id: str
    age: int
    department_id: int
    hire_date: date
    job_title_id: int
    hourly_rate: float

    class Config:
        """Configuration for the EmployeeSchema."""

        orm_mode = True

