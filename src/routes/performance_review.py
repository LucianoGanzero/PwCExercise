"""Module for managing performance review routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from starlette.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

from src.config.db import get_db
from src.models.performance_review import PerformanceReview
from src.schemas.performance_review import PerformanceReviewSchema

performance_review_router = APIRouter()

@performance_review_router.get(
                            "/",
                            response_model=list[PerformanceReviewSchema],
                            tags=["performance_reviews"],
                        )
def get_performance_reviews(db: Annotated[Session, Depends(get_db)]) -> list:
    """Retrieve all performance reviews from the database.

    Returns:
        list: A list of all performance reviews.

    """
    return db.query(PerformanceReview).all()

@performance_review_router.post(
                            "/",
                            response_model=PerformanceReviewSchema,
                            tags=["performance_reviews"],
                        )
def create_performance_review(
            performance_review: PerformanceReviewSchema,
            db: Annotated[Session, Depends(get_db)],
        ) -> dict:
    """Create a new performance review in the database.

    Args:
        performance_review (PerformanceReview): The performance review data to create.
        db (Session): The database session.

    Returns:
        dict: The created performance review data.

    """
    new_performance_review = PerformanceReview(
        employee_id=performance_review.employee_id,
        review_date=performance_review.review_date,
        score=performance_review.score,
        comments=performance_review.comments,
    )
    db.add(new_performance_review)
    db.commit()
    return new_performance_review

@performance_review_router.get("/{performance_review_id}",
                response_model=PerformanceReviewSchema,
                tags=["performance_reviews"])
def get_performance_review(
                        performance_review_id: int,
                        db: Annotated[Session, Depends(get_db)],
                    ) -> dict:
    """Retrieve a performance review from the database by ID.

    Args:
        performance_review_id (int): The ID of the performance review to retrieve.
        db (Session): The database session.

    Returns:
        dict: The performance review data or a 404 response if not found.

    """
    performance_review = (
                        db.query(PerformanceReview)
                        .filter(PerformanceReview.id == performance_review_id)
                        .first()
                    )
    if performance_review is None:
        return Response(status_code=HTTP_404_NOT_FOUND)
    return performance_review

@performance_review_router.put("/{performance_review_id}",
                response_model=PerformanceReviewSchema,
                tags=["performance_reviews"])
def update_performance_review(
                performance_review_id: int,
                performance_review: PerformanceReviewSchema,
                db: Annotated[Session, Depends(get_db)],
            ) -> dict:
    """Update a performance review in the database by ID.

    Args:
        performance_review_id (int): The ID of the performance review to update.
        performance_review (PerformanceReview): The performance review data to update.
        db (Session): The database session.

    Returns:
        dict: The updated performance review data or a 404 response if not found.

    """
    performance_review_data = (
                        db.query(PerformanceReview)
                        .filter(PerformanceReview.id == performance_review_id)
                        .first()
                    )
    if performance_review_data is None:
        return Response(status_code=HTTP_404_NOT_FOUND)
    for key, value in performance_review.dict(exclude_unset=True).items():
        setattr(performance_review_data, key, value)
    db.commit()
    return performance_review_data

@performance_review_router.delete("/{performance_review_id}",
                status_code=status.HTTP_204_NO_CONTENT,
                tags=["performance_reviews"])
def delete_performance_review(
                performance_review_id: int,
                db: Annotated[Session, Depends(get_db)],
            ) -> Response:
    """Delete a performance review from the database by ID.

    Args:
        performance_review_id (int): The ID of the performance review to delete.
        db (Session): The database session.

    Returns:
        Response: An empty response with a 204 status code.

    """
    performance_review = (
                        db.query(PerformanceReview)
                        .filter(PerformanceReview.id == performance_review_id)
                        .first()
                    )
    if performance_review is None:
        return Response(status_code=HTTP_404_NOT_FOUND)

    db.delete(performance_review)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)
