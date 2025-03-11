"""Module containing the schema definition for employee data."""

from datetime import date

from pydantic import BaseModel

from .department import DepartmentSchema
from .job_title import JobTitleSchema
from .performance_review import PerformanceReviewSchema
from .salary import SalarySchema


class EmployeeSchema(BaseModel):
    """Schema for employee data."""

    id: int
    emp_id: str
    age: int
    department_id: int
    hire_date: date
    job_title_id: int
    hourly_rate: float
    performance_reviews: list[PerformanceReviewSchema] = []
    salaries: list[SalarySchema] = []
    job_title: JobTitleSchema
    department: DepartmentSchema

    class Config:
        """Configuration for the EmployeeSchema."""

        orm_mode = True

