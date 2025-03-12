"""Defines the SalarySchema for salary data."""

from datetime import date

from pydantic import BaseModel


class SalaryCreateSchema(BaseModel):
    """Schema for salary data creation."""

    employee_id: int
    monthly_income: float
    effective_date: date
    hourly_rate: float

    class Config:
        """Configuration for SalarySchema."""

        orm_mode = True

class SalarySchema(BaseModel):
    """Schema for salary data."""

    id: int
    employee_id: int
    monthly_income: float
    effective_date: date
    hourly_rate: float

    class Config:
        """Configuration for SalarySchema."""

        orm_mode = True
