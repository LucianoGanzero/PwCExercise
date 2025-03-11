"""Module providing API routes for managing salaries."""

from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from starlette.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

from src.pwcexercise.config.db import get_db
from src.pwcexercise.models.salary import Salary
from src.pwcexercise.schemas.salary import SalarySchema

salary_router = APIRouter()

@salary_router.get("/", response_model=list[SalarySchema], tags=["salaries"])
def get_salaries(db: Annotated[Session, Depends(get_db)]) -> list:
    """Retrieve all salaries from the database.

    Returns:
        list: A list of all salaries.

    """
    return db.query(Salary).all()

@salary_router.post("/", response_model=SalarySchema, tags=["salaries"])
def create_salary(
                salary: SalarySchema,
                db: Annotated[Session, Depends(get_db)],
            ) -> dict:
    """Create a new salary in the database.

    Args:
        salary (Salary): The salary data to create.
        db (Session): The database session.

    Returns:
        dict: The created salary data.

    """
    new_salary = Salary(
                    employee_id=salary.employee_id,
                    salary_amount=salary.salary_amount,
                    effective_date=salary.effective_date,
                )
    db.add(new_salary)
    db.commit()
    return new_salary

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
    salary = db.query(Salary).filter(Salary.id == salary_id).first()
    if salary is None:
        return Response(status_code=HTTP_404_NOT_FOUND)
    return salary

@salary_router.put("/{salary_id}", response_model=SalarySchema, tags=["salaries"])
def update_salary(
                salary_id: int,
                salary: SalarySchema,
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
    db.query(Salary).filter(Salary.id == salary_id).update(salary.dict())
    db.commit()
    return db.query(Salary).filter(Salary.id == salary_id).first()

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
    salary = db.query(Salary).filter(Salary.id == salary_id).first()
    if salary is None:
        return Response(status_code=HTTP_404_NOT_FOUND)

    db.delete(salary)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)
