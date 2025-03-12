"""Provides services for managing departments in the database."""
from __future__ import annotations

from sqlalchemy.orm import Session

from src.pwcexercise.models.department import Department
from src.pwcexercise.models.employee import Employee
from src.pwcexercise.models.performance_review import PerformanceReview
from src.pwcexercise.models.salary import Salary
from src.pwcexercise.schemas.department import DepartmentCreateSchema, DepartmentSchema


def get_all_departments(db: Session) -> list:
    """Retrieve all departments from the database.

    :param db: Database session
    :return: List of all departments
    """
    return db.query(Department).all()

def create_department(department: DepartmentCreateSchema, db: Session) -> Department:
    """Create a new department in the database.

    :param department: Department data
    :param db: Database session
    :return: The created department
    """
    new_department = Department(name=department.name)
    db.add(new_department)
    db.commit()
    db.refresh(new_department)
    return new_department

def get_department_by_id(department_id: int, db: Session) -> Department | None:
    """Retrieve a department by its ID.

    :param department_id: ID of the department
    :param db: Database session
    :return: The department with the given ID or None if not found
    """
    return db.query(Department).filter(Department.id == department_id).first()

def update_department(
                department_id: int, department: DepartmentCreateSchema, db: Session,
            ) -> Department:
    """Update an existing department in the database.

    :param department_id: ID of the department to update
    :param department: Updated department data
    :param db: Database session
    :return: The updated department or None if not found
    """
    db_department = db.query(Department).filter(Department.id == department_id).first()
    if db_department:
        db_department.name = department.name
        db.commit()
        db.refresh(db_department)
    return db_department

def delete_department(department_id: int, db: Session) -> bool:
    """Delete a department from the database.

    :param department_id: ID of the department to delete
    :param db: Database session
    :return: True if the department was deleted, False otherwise
    """
    db_department = db.query(Department).filter(Department.id == department_id).first()
    if db_department:
        db.delete(db_department)
        db.commit()
        return True
    return False

def get_medium_salary_by_department(department_id: int, db: Session) -> float:
    """Calculate the average salary for a given department.

    This function retrieves all employees in the specified department and calculates
    the average of their most recent monthly salaries.

    Args:
        department_id (int): The ID of the department.
        db (Session): The database session used to query the database.

    Returns:
        float: The average salary of the employees in the department.
        Returns 0 if there are no employees or no salaries found.

    """
    employees = db.query(Employee).filter(Employee.department_id == department_id).all()

    if not employees:
        return 0

    total_salary = 0
    total_employees = 0

    for employee in employees:
        last_salary = db.query(Salary).filter(
            Salary.employee_id == employee.id,
        ).order_by(Salary.effective_date.desc()).first()

        if last_salary:
            total_salary += last_salary.monthly_income
            total_employees += 1

    if total_employees == 0:
        return 0

    return round(total_salary / total_employees, 2)

def get_average_performance_score_by_department(
                                department_id: int, db: Session) -> float:
    """Calculate the average performance score for a given department.

    Args:
        department_id (int): The ID of the department.
        db (Session): The database session.

    Returns:
        float: The average performance score of the department.
        Returns 0 if there are no employees or no performance reviews.

    """
    employees = db.query(Employee).filter(Employee.department_id == department_id).all()

    if not employees:
        return 0

    total_score = 0
    total_employees = 0


    for employee in employees:
        last_review = db.query(PerformanceReview).filter(
            PerformanceReview.employee_id == employee.id,
        ).order_by(PerformanceReview.review_date.desc()).first()

        if last_review:
            total_score += last_review.score
            total_employees += 1


    if total_employees == 0:
        return 0

    return round(total_score / total_employees, 2)
