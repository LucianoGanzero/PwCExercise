"""Module containing routes for employee-related operations."""

from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from starlette.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

from src.config.db import get_db
from src.models.employee import Employee
from src.schemas.employee import EmployeeSchema

employee = APIRouter()


@employee.get("/", response_model=list[EmployeeSchema], tags=["employees"])
def get_employees(db: Annotated[Session, Depends(get_db)]) -> list:
    """Retrieve all employees from the database.

    Returns:
        list: A list of all employees.

    """
    return db.query(Employee).all()


@employee.post("/", response_model=EmployeeSchema, tags=["employees"])
def create_employee(
                employee: EmployeeSchema,
                db: Annotated[Session, Depends(get_db)],
            ) -> dict:
    """Create a new employee in the database.

    Args:
        employee (Employee): The employee data to create.
        db (Session): The database session.

    Returns:
        dict: The created employee data.

    """
    new_employee = Employee(
                    emp_id=employee.emp_id,
                    age=employee.age,
                    department_id=employee.department_id,
                    hire_date=employee.hire_date,
                    job_title=employee.job_title,
                    status=employee.status,
                )
    db.add(new_employee)
    db.commit()
    return new_employee


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
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if employee is None:
        return Response(status_code=HTTP_404_NOT_FOUND)
    return employee


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
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if employee is None:
        return Response(status_code=HTTP_404_NOT_FOUND)

    db.delete(employee)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)


@employee.put("/{employee_id}",
                response_model=EmployeeSchema,
                tags=["employees"])
def update_employee(
        employee_id: int,
        employee: EmployeeSchema,
        db: Annotated[Session, Depends(get_db)]) -> dict:
    """Update an employee in the database by ID.

    Args:
        employee_id (int): The ID of the employee to update.
        employee (Employee): The new employee data.
        db (Session): The database session.

    Returns:
        dict: The updated employee data.

    """
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if db_employee is None:
        return Response(status_code=HTTP_404_NOT_FOUND)

    db_employee.name = employee.name
    db_employee.department_id = employee.department_id
    db_employee.hire_date = employee.hire_date
    db_employee.job_title = employee.job_title
    db_employee.status = employee.status

    db.commit()
    db.refresh(db_employee)
    return db_employee
