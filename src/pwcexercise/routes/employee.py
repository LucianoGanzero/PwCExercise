"""Module containing routes for employee-related operations."""

from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from src.pwcexercise.config.db import get_db
from src.pwcexercise.schemas.employee import EmployeeCreateSchema, EmployeeSchema
from src.pwcexercise.services import employee_service

employee = APIRouter()


@employee.get("/", response_model=list[EmployeeSchema], tags=["employees"])
def get_employees(db: Annotated[Session, Depends(get_db)]) -> list:
    """Retrieve all employees from the database.

    Returns:
        list: A list of all employees.

    """
    return employee_service.get_all_employees(db)


@employee.post("/", response_model=EmployeeSchema, tags=["employees"])
def create_employee(
                employee: EmployeeCreateSchema,
                db: Annotated[Session, Depends(get_db)],
            ) -> dict:
    """Create a new employee in the database.

    Args:
        employee (Employee): The employee data to create.
        db (Session): The database session.

    Returns:
        dict: The created employee data.

    """
    return employee_service.create_employee(employee, db)


@employee.get("/{employee_id}",
                response_model=EmployeeSchema,
                tags=["employees"])
def get_employee(employee_id: int, db: Annotated[Session, Depends(get_db)]) -> dict:
    """Retrieve an employee from the database by ID.

    Args:
        employee_id (int): The ID of the employee to retrieve.
        db (Session): The database session.

    Returns:
        dict: The employee data or a 404 response if not found.

    """
    return employee_service.get_employee_by_id(employee_id, db)


@employee.delete("/{employee_id}",
                status_code=status.HTTP_204_NO_CONTENT,
                tags=["employees"])
def delete_employee(
                employee_id: int,
                db: Annotated[Session, Depends(get_db)],
            ) -> Response:
    """Delete an employee from the database by ID.

    Args:
        employee_id (int): The ID of the employee to delete.
        db (Session): The database session.

    Returns:
        Response: An empty response with a 204 status code.

    """
    if employee_service.delete_employee(employee_id, db):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@employee.put("/{employee_id}",
                response_model=EmployeeSchema,
                tags=["employees"])
def update_employee(
        employee_id: int,
        employee: EmployeeCreateSchema,
        db: Annotated[Session, Depends(get_db)]) -> dict:
    """Update an employee in the database by ID.

    Args:
        employee_id (int): The ID of the employee to update.
        employee (Employee): The new employee data.
        db (Session): The database session.

    Returns:
        dict: The updated employee data.

    """
    updated_employee = employee_service.update_employee(employee_id, employee, db)
    if updated_employee is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return updated_employee
