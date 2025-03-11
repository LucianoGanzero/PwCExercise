"""Defines the Salary model representing the salary details of an employee."""

from sqlalchemy import Column, Date, Float, ForeignKey, Integer

from .base import Base


class Salary(Base):
    """Salary model representing the salary details of an employee."""

    __tablename__ = "salaries"
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    salary_amount = Column(Float, nullable=False)
    effective_date = Column(Date, nullable=False)
