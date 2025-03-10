from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from datetime import date


class PerformanceReviewSchema(BaseModel):
    """Schema for performance review data."""

    id: int
    employee_id: int
    review_date: date
    score: int
    comments: str | None = None

    class Config:
        """Configuration for the PerformanceReviewSchema."""

        orm_mode = True
