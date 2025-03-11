"""Module providing API routes for managing salaries."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from starlette.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

from src.pwcexercise.config.db import get_db
from src.pwcexercise.schemas.salary import SalaryCreateSchema, SalarySchema
from src.pwcexercise.services import salary_service
from src.pwcexercise.services.employee_service import get_employee_by_id

salary_router = APIRouter()

@salary_router.get("/", response_model=list[SalarySchema], tags=["salaries"])
def get_salaries(db: Annotated[Session, Depends(get_db)]) -> list:
    """Retrieve all salaries from the database.

    Returns:
        list: A list of all salaries.

    """
    return salary_service.get_all_salaries(db)

@salary_router.post("/", response_model=SalarySchema, tags=["salaries"])
def create_salary(
                salary: SalaryCreateSchema,
                db: Annotated[Session, Depends(get_db)],
            ) -> dict:
    """Create a new salary in the database.

    Args:
        salary (Salary): The salary data to create.
        db (Session): The database session.

    Returns:
        dict: The created salary data.

    """
    employee = get_employee_by_id(salary.employee_id, db)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return salary_service.create_salary(salary, db)

@salary_router.get("/{salary_id}",
                response_model=SalarySchema,
                tags=["salaries"])
def get_salary(salary_id: int, db: Annotated[Session, Depends(get_db)]) -> dict:
    """Retrieve a salary from the database by ID.

    Args:
        salary_id (int): The
        ID of the salary to retrieve.
        db (Session): The database session.

    Returns:
        dict: The salary data or a 404 response if not found.

    """
    salary = salary_service.get_salary_by_id(salary_id, db)
    if salary is None:
        return Response(status_code=HTTP_404_NOT_FOUND)
    return salary

@salary_router.put("/{salary_id}", response_model=SalarySchema, tags=["salaries"])
def update_salary(
                salary_id: int,
                salary: SalaryCreateSchema,
                db: Annotated[Session, Depends(get_db)],
            ) -> dict:
    """Update a salary in the database by ID.

    Args:
        salary_id (int): The ID of the salary to update.
        salary (Salary): The salary data to update.
        db (Session): The database session.

    Returns:
        dict: The updated salary data or a 404 response if not found.

    """
    employee = get_employee_by_id(salary.employee_id, db)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    updated_job_title = salary_service.update_salary(salary_id, salary, db)
    if updated_job_title is None:
        return Response(status_code=HTTP_404_NOT_FOUND)
    return updated_job_title

@salary_router.delete(
                    "/{salary_id}",
                    status_code=status.HTTP_204_NO_CONTENT,
                    tags=["salaries"],
                )
def delete_salary(salary_id: int, db: Annotated[Session, Depends(get_db)]) -> Response:
    """Delete a salary from the database by ID.

    Args:
        salary_id (int): The
        ID of the salary to delete.
        db (Session): The database session.

    Returns:
        Response: An empty response with a 204 status code.

    """
    success = salary_service.delete_salary(salary_id, db)
    if not success:
        return Response(status_code=HTTP_404_NOT_FOUND)
    return Response(status_code=HTTP_204_NO_CONTENT)
