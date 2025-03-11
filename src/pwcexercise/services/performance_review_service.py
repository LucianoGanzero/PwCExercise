from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.pwcexercise.models.performance_review import PerformanceReview
from src.pwcexercise.schemas.performance_review import PerformanceReviewCreateSchema


def get_all_performance_reviews(db: Session) -> list:
    """Retrieve all performance reviews from the database."""
    return db.query(PerformanceReview).all()


def create_performance_review(
                            performance_review: PerformanceReviewCreateSchema,
                            db: Session,
                        ) -> PerformanceReview:
    """Create a new performance review in the database."""
    new_performance_review = PerformanceReview(
        employee_id=performance_review.employee_id,
        review_date=performance_review.review_date,
        score=performance_review.score,
        comments=performance_review.comments,
    )
    db.add(new_performance_review)
    db.commit()
    db.refresh(new_performance_review)
    return new_performance_review


def get_performance_review_by_id(
                            performance_review_id: int, db: Session,
                        ) -> PerformanceReview:
    """Retrieve a performance review by ID."""
    return (
        db.query(PerformanceReview)
        .filter(PerformanceReview.id == performance_review_id)
        .first()
    )


def update_performance_review(
                            performance_review_id: int,
                            performance_review: PerformanceReviewCreateSchema,
                            db: Session,
                        ) -> PerformanceReview:
    """Update a performance review in the database by ID."""
    performance_review_data = (
        db.query(PerformanceReview)
        .filter(PerformanceReview.id == performance_review_id)
        .first()
    )
    if performance_review_data:
        for key, value in performance_review.dict(exclude_unset=True).items():
            setattr(performance_review_data, key, value)

        db.commit()
        db.refresh(performance_review_data)
    return performance_review_data


def delete_performance_review(performance_review_id: int, db: Session) -> bool:
    """Delete a performance review from the database by ID."""
    performance_review = (
        db.query(PerformanceReview)
        .filter(PerformanceReview.id == performance_review_id)
        .first()
    )
    if performance_review:
        db.delete(performance_review)
        db.commit()
        return True
    return False
