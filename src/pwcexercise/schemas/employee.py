"""Module containing the schema definition for employee data."""
from __future__ import annotations

from datetime import date

from pydantic import BaseModel

from .department import DepartmentSchema
from .job_title import JobTitleSchema
from .performance_review import PerformanceReviewSchema
from .salary import SalarySchema


class EmployeeCreateSchema(BaseModel):
    """Schema for creating employee data."""

    emp_id: str
    age: int
    department_id: int
    hire_date: date
    job_title_id: int
    hourly_rate: float

    class Config:
        """Configuration for the EmployeeCreateSchema."""

        orm_mode = True

class EmployeeSchema(BaseModel):
    """Schema for employee data."""

    id: int
    emp_id: str
    age: int
    department_id: int
    hire_date: date
    job_title_id: int | None = None
    hourly_rate: float
    performance_reviews: list[PerformanceReviewSchema] = []
    salaries: list[SalarySchema] = []

    job_title: JobTitleSchema | None = None
    department: DepartmentSchema | None = None

    class Config:
        """Configuration for the EmployeeSchema."""

        orm_mode = True

