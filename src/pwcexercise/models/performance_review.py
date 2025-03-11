"""Defines the PerformanceReview model for an employee's performance evaluation."""

from sqlalchemy import Column, Date, ForeignKey, Integer, String

from .base import Base


class PerformanceReview(Base):
    """Performance Review model representing an employee's performance evaluation."""

    __tablename__ = "performance_reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    review_date = Column(Date, nullable=False)
    score = Column(Integer, nullable=False)
    comments = Column(String, nullable=True)

