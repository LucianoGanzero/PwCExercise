"""Module containing routes for managing job titles."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from starlette.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

from src.pwcexercise.config.db import get_db
from src.pwcexercise.schemas.employee import EmployeeSchema
from src.pwcexercise.schemas.job_title import JobTitleCreateSchema, JobTitleSchema
from src.pwcexercise.services import job_title_service

job_title_router = APIRouter()

@job_title_router.get("/", response_model=list[JobTitleSchema], tags=["job_titles"])
def get_job_titles(db: Annotated[Session, Depends(get_db)]) -> list:
    """Retrieve all job titles from the database.

    Returns:
        list: A list of all job titles.

    """
    return job_title_service.get_all_job_titles(db)

@job_title_router.post("/", response_model=JobTitleSchema, tags=["job_titles"])
def create_job_title(
            job_title: JobTitleCreateSchema,
            db: Annotated[Session, Depends(get_db)],
        ) -> dict:
    """Create a new job title in the database.

    Args:
        job_title (JobTitle): The job title data to create.
        db (Session): The database session.

    Returns:
        dict: The created job title data.

    """
    return job_title_service.create_job_title(job_title, db)

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
    job_title = job_title_service.get_job_title_by_id(job_title_id, db)
    if job_title is None:
        return Response(status_code=HTTP_404_NOT_FOUND)
    return job_title

@job_title_router.put("/{job_title_id}",
                response_model=JobTitleSchema,
                tags=["job_titles"])
def update_job_title(
            job_title_id: int,
            job_title: JobTitleCreateSchema,
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
    updated_job_title = job_title_service.update_job_title(job_title_id, job_title, db)
    if updated_job_title is None:
        return Response(status_code=HTTP_404_NOT_FOUND)
    return updated_job_title

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
    success = job_title_service.delete_job_title(job_title_id, db)
    if not success:
        return Response(status_code=HTTP_404_NOT_FOUND)
    return Response(status_code=HTTP_204_NO_CONTENT)

@job_title_router.get("/{job_title_id}/employees",
                    response_model=list[EmployeeSchema],
                    tags=["job_titles"])
def get_employees_by_job_title(
    job_title_id: int, db: Annotated[Session, Depends(get_db)]) -> list:
    """Retrieve all employees associated with a job title by ID.

    Args:
        job_title_id (int): The ID of the job title to retrieve employees for.
        db (Session): The database session.

    Returns:
        list: A list of employees associated with the job title.

    """
    job_title = job_title_service.get_job_title_by_id(job_title_id, db)
    if job_title is None:
        raise HTTPException(status_code=404, detail="Job title not found")
    employees = job_title_service.get_employees_by_job_title(job_title_id, db)
    if not employees:
        raise HTTPException(
            status_code=404,
            detail="No employees found with this job title")
    return employees

@job_title_router.get("/{job_title_id}/medium_salary", tags=["job_titles"])
def get_medium_salary_by_job_title(
                        job_title_id: int,
                        db: Annotated[Session, Depends(get_db)]) -> dict:
    """Retrieve the average salary of the job title with the given ID."""
    job_title = job_title_service.get_job_title_by_id(job_title_id, db)
    if job_title is None:
        raise HTTPException(status_code=404, detail="Job title not found")

    medium_salary = job_title_service.get_medium_salary_by_job_title(job_title_id, db)

    if medium_salary == 0:
        raise HTTPException(
            status_code=404,
            detail="No employees found with this job title")

    return {"job_title_id": job_title_id, "medium_salary": medium_salary}

@job_title_router.get("/{job_title_id}/average_performance_score", tags=["job_titles"])
def get_average_performance_score_by_job_title(
                    job_title_id: int,
                    db: Annotated[Session, Depends(get_db)]) -> dict:
    """Retrieve the average performance score of the job title with the given ID."""
    job_title = job_title_service.get_job_title_by_id(job_title_id, db)
    if job_title is None:
        raise HTTPException(status_code=404, detail="Job title not found")

    average_score = job_title_service.get_average_performance_score_by_job_title(
                                                                job_title_id, db)

    if average_score == 0:
        raise HTTPException(
            status_code=404,
            detail="No performance reviews found for employees with this job title")

    return {"job_title_id": job_title_id, "average_performance_score": average_score}

