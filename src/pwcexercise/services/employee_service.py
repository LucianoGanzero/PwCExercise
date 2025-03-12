"""Provides services for managing employees in the database."""
from __future__ import annotations

from sqlalchemy.orm import Session

from src.pwcexercise.models.employee import Employee
from src.pwcexercise.models.performance_review import PerformanceReview
from src.pwcexercise.models.salary import Salary
from src.pwcexercise.schemas.employee import EmployeeCreateSchema, EmployeeSchema


def get_all_employees(db: Session) -> list:
    """Retrieve all employees from the database.

    :param db: Database session
    :return: List of all employees
    """
    return db.query(Employee).all()

def create_employee(employee: EmployeeCreateSchema, db: Session) -> Employee:
    """Create a new employee in the database.

    :param employee: Employee data
    :param db: Database session
    :return: The created employee
    """
    new_employee = Employee(
        emp_id=employee.emp_id,
        age=employee.age,
        department_id=employee.department_id,
        hire_date=employee.hire_date,
        job_title_id=employee.job_title_id,
    )
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee

def get_employee_by_id(employee_id: int, db: Session) -> Employee | None:
    """Retrieve an employee by their ID.

    :param employee_id: ID of the employee
    :param db: Database session
    :return: The employee with the given ID or None if not found
    """
    return db.query(Employee).filter(Employee.id == employee_id).first()

def update_employee(
                employee_id: int, employee: EmployeeCreateSchema, db: Session,
            ) -> Employee:
    """Update an existing employee in the database.

    :param employee_id: ID of the employee to update
    :param employee: Updated employee data
    :param db: Database session
    :return: The updated employee or None if not found
    """
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if db_employee:
        db_employee.emp_id = employee.emp_id
        db_employee.age = employee.age
        db_employee.department_id = employee.department_id
        db_employee.hire_date = employee.hire_date
        db_employee.job_title_id = employee.job_title_id
        db.commit()
        db.refresh(db_employee)
    return db_employee

def delete_employee(employee_id: int, db: Session) -> bool:
    """Delete an employee from the database.

    :param employee_id: ID of the employee to delete
    :param db: Database session
    :return: True if the employee was deleted, False otherwise
    """
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if db_employee:
        db.delete(db_employee)
        db.commit()
        return True
    return False

def get_active_salary(employee_id: int, db: Session) -> Salary:
    """Retrieve the active salary of an employee.

    :param employee_id: ID of the employee
    :param db: Database session
    :return: The active salary of the employee
    """
    return (
        db.query(Salary)
        .filter(Salary.employee_id == employee_id)
        .order_by(Salary.effective_date.desc())
        .first()
    )

def get_latest_performance_review(employee_id: int, db: Session) -> PerformanceReview:
    """Retrieve the latest performance review of an employee.

    :param employee_id: ID of the employee
    :param db: Database session
    :return: The latest performance review of the employee
    """
    return (
        db.query(PerformanceReview)
        .filter(PerformanceReview.employee_id == employee_id)
        .order_by(PerformanceReview.review_date.desc())
        .first()
    )
