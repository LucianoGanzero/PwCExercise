"""Defines the SalarySchema for salary data."""

from datetime import date

from pydantic import BaseModel


class SalaryCreateSchema(BaseModel):
    """Schema for salary data creation."""

    employee_id: int
    salary_amount: float
    effective_date: date

    class Config:
        """Configuration for SalarySchema."""

        orm_mode = True

class SalarySchema(BaseModel):
    """Schema for salary data."""

    id: int
    employee_id: int
    salary_amount: float
    effective_date: date

    class Config:
        """Configuration for SalarySchema."""

        orm_mode = True
