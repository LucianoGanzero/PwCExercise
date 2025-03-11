"""Defines the Employee model for the database."""

from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Employee(Base):
    """Employee model representing an employee record."""

    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, autoincrement=True)
    emp_id = Column(String, nullable=False)
    age = Column(Integer)
    department_id = Column(Integer, ForeignKey("departments.id"))
    hire_date = Column(Date)
    job_title_id = Column(Integer, ForeignKey("job_titles.id"))
    hourly_rate = Column(Float)

    department = relationship("Department", backref="employees")
    job_title = relationship("JobTitle", backref="employees")
    salaries = relationship("Salary", cascade="all, delete-orphan")
    performance_reviews = relationship(
        "PerformanceReview", cascade="all, delete-orphan",
    )


