"""Provides services for managing departments in the database."""
from __future__ import annotations

from sqlalchemy.orm import Session

from src.pwcexercise.models.department import Department
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
