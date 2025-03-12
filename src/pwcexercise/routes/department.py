"""Module containing routes for department-related operations."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from src.pwcexercise.config.db import get_db
from src.pwcexercise.schemas.department import DepartmentCreateSchema, DepartmentSchema
from src.pwcexercise.services import department_service

department_router = APIRouter()

@department_router.get("/", response_model=list[DepartmentSchema], tags=["departments"])
def get_departments(db: Annotated[Session, Depends(get_db)]) -> list:
    """Retrieve all departments from the database.

    Returns:
        list: A list of all departments.

    """
    return department_service.get_all_departments(db)

@department_router.post("/", response_model=DepartmentSchema, tags=["departments"])
def create_department(
            department: DepartmentCreateSchema,
            db: Annotated[Session, Depends(get_db)],
        ) -> dict:
    """Create a new department in the database.

    Args:
        department (Department): The department data to create.
        db (Session): The database session.

    Returns:
        dict: The created department data.

    """
    return department_service.create_department(department, db)

@department_router.get("/{department_id}",
                response_model=DepartmentSchema,
                tags=["departments"])
def get_department(department_id: int, db: Annotated[Session, Depends(get_db)]) -> dict:
    """Retrieve a department by its ID.

    Args:
        department_id (int): The ID of the department to retrieve.
        db (Session): The database session.

    Returns:
        dict: The department data or a 404 response if not found.

    """
    department = department_service.get_department_by_id(department_id, db)
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return department

@department_router.put("/{department_id}",
                response_model=DepartmentSchema,
                tags=["departments"])
def update_department(
                department_id: int,
                department: DepartmentCreateSchema,
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
    updated_department = department_service.update_department(
                        department_id, department, db,
                    )
    if updated_department is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return updated_department

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
    if department_service.delete_department(department_id, db):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return Response(status_code=status.HTTP_404_NOT_FOUND)

@department_router.get("/{department_id}/medium_salary", tags=["departments"])
def get_medium_salary_by_id(department_id: int,
                            db: Annotated[Session, Depends(get_db)]) -> dict:
    """Retrieve the average salary of the department with the given ID."""
    department = department_service.get_department_by_id(department_id, db)
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")

    medium_salary = department_service.get_medium_salary_by_department(
                                                            department_id,
                                                            db)

    if medium_salary == 0:
        raise HTTPException(
            status_code=404,
            detail="No employees found in this department")

    return {"department_id": department_id, "medium_salary": medium_salary}

@department_router.get("/{department_id}/average_performance_score",
                        tags=["departments"])
def get_average_performance_score_by_id(
    department_id: int, db: Annotated[Session, Depends(get_db)],
) -> dict:
    """Retrieve the average performance score of the department with the given ID."""
    department = department_service.get_department_by_id(department_id, db)
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")

    average_score = department_service.get_average_performance_score_by_department(
        department_id, db)

    if average_score == 0:
        raise HTTPException(
            status_code=404, detail="No performance reviews found in this department")

    return {"department_id": department_id, "average_performance_score": average_score}
