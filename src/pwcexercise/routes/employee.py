"""Module containing routes for employee-related operations."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from src.pwcexercise.config.db import get_db
from src.pwcexercise.schemas.employee import EmployeeCreateSchema, EmployeeSchema
from src.pwcexercise.schemas.performance_review import PerformanceReviewSchema
from src.pwcexercise.schemas.salary import SalarySchema
from src.pwcexercise.services import employee_service, salary_service

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
    employee = employee_service.get_employee_by_id(employee_id, db)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
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

@employee.get("/{employee_id}/active_salary",
                tags=["employees"])
def get_active_salary_of_employee(
                    employee_id: int,
                    db: Annotated[Session, Depends(get_db)]) -> dict:
    """Retrieve the active salary of the employee with the given ID."""
    employee = employee_service.get_employee_by_id(employee_id, db)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    salary = employee_service.get_active_salary(employee_id, db)
    if salary is None:
        raise HTTPException(
            status_code=404,
            detail="This employee does not have a salary")
    salary_data = SalarySchema.from_orm(salary)

    return {"active_salary": salary_data.dict()}

@employee.get("/{employee_id}/latest_performance_review",
                tags=["employees"])
def get_latest_performance_review_of_employee(
                employee_id: int,
                db: Annotated[Session, Depends(get_db)]) -> dict:
    """Retrieve the latest performance review of the employee with the given ID."""
    employee = employee_service.get_employee_by_id(employee_id, db)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    performance_review = employee_service.get_latest_performance_review(employee_id, db)
    if performance_review is None:
        raise HTTPException(
            status_code=404,
            detail="This employee does not have any performance review")
    performance_data = PerformanceReviewSchema.from_orm(performance_review)

    return {"latest_performance_review": performance_data.dict()}

@employee.get("/{employee_id}/aguinaldo",
               tags=["employees"])
def get_aguinaldo_of_employee(
                    employee_id: int,
                    db: Annotated[Session, Depends(get_db)]) -> dict:
    """Retrieve the aguinaldo for the employee with the given ID.

    The aguinaldo is half of the highest salary in the last six months.
    """
    employee = employee_service.get_employee_by_id(employee_id, db)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    highest_salary = salary_service.get_highest_salary_in_last_six_months(
        employee_id, db)
    if not highest_salary:
        raise HTTPException(
            status_code=404,
            detail="This employee does not have any salary in the last six months")

    aguinaldo = round(highest_salary.monthly_income / 2, 2)

    return {"id": employee_id, "empID": employee.emp_id,"aguinaldo": aguinaldo}


@employee.get("/{employee_id}/hours_worked", tags=["employees"])
def get_employee_hours_worked(
                    employee_id: int,
                    db: Annotated[Session, Depends(get_db)]) -> dict:
    """Retrieve the hours worked by the employee with the given ID."""
    employee = employee_service.get_employee_by_id(employee_id, db)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    salary = employee_service.get_active_salary(employee_id, db)
    if salary is None:
        raise HTTPException(
            status_code=404,
            detail="This employee does not have a salary")

    hours_worked = 0

    if salary.hourly_rate is not None:
        if salary.hourly_rate > 0:
            hours_worked = round(salary.monthly_income / salary.hourly_rate, 2)
        else:
            raise HTTPException(status_code=400, detail="Invalid data")

    return {"employee_id": employee_id, "hours_worked": hours_worked}
