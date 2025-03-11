"""Module for managing performance review routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from starlette.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

from src.pwcexercise.config.db import get_db
from src.pwcexercise.schemas.performance_review import (
    PerformanceReviewCreateSchema,
    PerformanceReviewSchema,
)
from src.pwcexercise.services import performance_review_service
from src.pwcexercise.services.employee_service import get_employee_by_id

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
    return performance_review_service.get_all_performance_reviews(db)

@performance_review_router.post(
                            "/",
                            response_model=PerformanceReviewSchema,
                            tags=["performance_reviews"],
                        )
def create_performance_review(
            performance_review: PerformanceReviewCreateSchema,
            db: Annotated[Session, Depends(get_db)],
        ) -> dict:
    """Create a new performance review in the database.

    Args:
        performance_review (PerformanceReview): The performance review data to create.
        db (Session): The database session.

    Returns:
        dict: The created performance review data.

    """
    employee = get_employee_by_id(performance_review.employee_id, db)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return performance_review_service.create_performance_review(performance_review, db)

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
    performance_review = performance_review_service.get_performance_review_by_id(
                        performance_review_id, db,
                    )
    if performance_review is None:
        return Response(status_code=HTTP_404_NOT_FOUND)
    return performance_review

@performance_review_router.put("/{performance_review_id}",
                response_model=PerformanceReviewSchema,
                tags=["performance_reviews"])
def update_performance_review(
                performance_review_id: int,
                performance_review: PerformanceReviewCreateSchema,
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
    employee = get_employee_by_id(performance_review.employee_id, db)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return performance_review_service.update_performance_review(
                performance_review_id, performance_review, db,
            )

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
    success = performance_review_service.delete_performance_review(
        performance_review_id, db)
    if not success:
        return Response(status_code=HTTP_404_NOT_FOUND)
    return Response(status_code=HTTP_204_NO_CONTENT)
