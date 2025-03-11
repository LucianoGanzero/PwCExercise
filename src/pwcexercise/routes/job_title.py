"""Module containing routes for managing job titles."""

from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from starlette.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

from src.pwcexercise.config.db import get_db
from src.pwcexercise.models.job_title import JobTitle
from src.pwcexercise.schemas.job_title import JobTitleSchema

job_title_router = APIRouter()

@job_title_router.get("/", response_model=list[JobTitleSchema], tags=["job_titles"])
def get_job_titles(db: Annotated[Session, Depends(get_db)]) -> list:
    """Retrieve all job titles from the database.

    Returns:
        list: A list of all job titles.

    """
    return db.query(JobTitle).all()

@job_title_router.post("/", response_model=JobTitleSchema, tags=["job_titles"])
def create_job_title(
            job_title: JobTitleSchema,
            db: Annotated[Session, Depends(get_db)],
        ) -> dict:
    """Create a new job title in the database.

    Args:
        job_title (JobTitle): The job title data to create.
        db (Session): The database session.

    Returns:
        dict: The created job title data.

    """
    new_job_title = JobTitle(title=job_title.title)
    db.add(new_job_title)
    db.commit()
    return new_job_title

@job_title_router.get("/{job_title_id}",
                response_model=JobTitleSchema,
                tags=["job_titles"])
def get_job_title(job_title_id: int, db: Annotated[Session, Depends(get_db)]) -> dict:
    """Retrieve a job title from the database by ID.

    Args:
        job_title_id (int): The ID of the job title to retrieve.
        db (Session): The database session.

    Returns:
        dict: The job title data or a 404 response if not found.

    """
    job_title = db.query(JobTitle).filter(JobTitle.id == job_title_id).first()
    if job_title is None:
        return Response(status_code=HTTP_404_NOT_FOUND)
    return job_title

@job_title_router.put("/{job_title_id}",
                response_model=JobTitleSchema,
                tags=["job_titles"])
def update_job_title(
            job_title_id: int,
            job_title: JobTitleSchema,
            db: Annotated[Session, Depends(get_db)],
        ) -> dict:
    """Update a job title in the database by ID.

    Args:
        job_title_id (int): The ID of the job title to update.
        job_title (JobTitle): The job title data to update.
        db (Session): The database session.

    Returns:
        dict: The updated job title data or a 404 response if not found.

    """
    job_title_to_update = db.query(JobTitle).filter(JobTitle.id == job_title_id).first()
    if job_title_to_update is None:
        return Response(status_code=HTTP_404_NOT_FOUND)
    job_title_to_update.title = job_title.title
    db.commit()
    return job_title_to_update

@job_title_router.delete("/{job_title_id}",
                status_code=status.HTTP_204_NO_CONTENT,
                tags=["job_titles"])
def delete_job_title(
            job_title_id: int,
            db: Annotated[Session, Depends(get_db)],
        ) -> Response:
    """Delete a job title from the database by ID.

    Args:
        job_title_id (int): The ID of the job title to delete.
        db (Session): The database session.

    Returns:
        Response: An empty response with a 204 status code.

    """
    job_title = db.query(JobTitle).filter(JobTitle.id == job_title_id).first()
    if job_title is None:
        return Response(status_code=HTTP_404_NOT_FOUND)

    db.delete(job_title)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)
