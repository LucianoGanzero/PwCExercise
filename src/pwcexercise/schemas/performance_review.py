"""Module for performance review schema."""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel


class PerformanceReviewCreateSchema(BaseModel):
    """Schema for performance review creation data."""

    employee_id: int
    review_date: date
    score: int
    comments: str | None = None

    class Config:
        """Configuration for the PerformanceReviewSchema."""

        from_attributes = True

class PerformanceReviewSchema(BaseModel):
    """Schema for performance review data."""

    id: int
    employee_id: int
    review_date: date
    score: int
    comments: str | None = None

    class Config:
        """Configuration for the PerformanceReviewSchema."""

        from_attributes = True
