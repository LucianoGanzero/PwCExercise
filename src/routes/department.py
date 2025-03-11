"""Module containing routes for department-related operations."""

from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from starlette.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

from src.config.db import get_db
from src.models.department import Department
from src.schemas.department import DepartmentSchema

department_router = APIRouter()

@department_router.get("/", response_model=list[DepartmentSchema], tags=["departments"])
def get_departments(db: Annotated[Session, Depends(get_db)]) -> list:
    """Retrieve all departments from the database.

    Returns:
        list: A list of all departments.

    """
    return db.query(Department).all()

@department_router.post("/", response_model=DepartmentSchema, tags=["departments"])
def create_department(
            department: DepartmentSchema,
            db: Annotated[Session, Depends(get_db)],
        ) -> dict:
    """Create a new department in the database.

    Args:
        department (Department): The department data to create.
        db (Session): The database session.

    Returns:
        dict: The created department data.

    """
    new_department = Department(name=department.name)
    db.add(new_department)
    db.commit()
    return new_department

@department_router.get("/{department_id}",
                response_model=DepartmentSchema,
                tags=["departments"])
def get_department(department_id: int, db: Annotated[Session, Depends(get_db)]) -> dict:
    """Retrieve a department from the database by ID.

    Args:
        department_id (int): The ID of the department to retrieve.
        db (Session): The database session.

    Returns:
        dict: The department data or a 404 response if not found.

    """
    department = db.query(Department).filter(Department.id == department_id).first()
    if department is None:
        return Response(status_code=HTTP_404_NOT_FOUND)
    return department

@department_router.put("/{department_id}",
                response_model=DepartmentSchema,
                tags=["departments"])
def update_department(
                department_id: int,
                department: DepartmentSchema,
                db: Annotated[Session, Depends(get_db)],
            ) -> dict:
    """Update a department in the database by ID.

    Args:
        department_id (int): The ID of the department to update.
        department (Department): The department data to update.
        db (Session): The database session.

    Returns:
        dict: The updated department data or a 404 response if not found.

    """
    department = db.query(Department).filter(Department.id == department_id).first()
    if department is None:
        return Response(status_code=HTTP_404_NOT_FOUND)
    department.name = department.name
    db.commit()
    return department

@department_router.delete("/{department_id}",
                status_code=status.HTTP_204_NO_CONTENT,
                tags=["departments"])
def delete_department(
                    department_id: int,
                    db: Annotated[Session, Depends(get_db)],
                ) -> Response:
    """Delete a department from the database by ID.

    Args:
        department_id (int): The ID of the department to delete.
        db (Session): The database session.

    Returns:
        Response: An empty response with a 204 status code.

    """
    department = db.query(Department).filter(Department.id == department_id).first()
    if department is None:
        return Response(status_code=HTTP_404_NOT_FOUND)
    db.delete(department)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)
