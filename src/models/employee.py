from sqlalchemy import Column, Date, ForeignKey, Integer, String

from .base import Base


class Employee(Base):
    """Employee model representing an employee record."""

    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))
    hire_date = Column(Date)
    job_title = Column(String)
    status = Column(String)
