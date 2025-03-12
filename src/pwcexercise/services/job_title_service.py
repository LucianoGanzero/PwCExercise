"""Provides services for managing job titles in the database."""

from sqlalchemy.orm import Session

from src.pwcexercise.models.employee import Employee
from src.pwcexercise.models.job_title import JobTitle
from src.pwcexercise.schemas.job_title import JobTitleCreateSchema
from src.pwcexercise.services import employee_service


def get_all_job_titles(db: Session) -> list:
    """Retrieve all job titles from the database."""
    return db.query(JobTitle).all()

def create_job_title(job_title: JobTitleCreateSchema, db: Session) -> JobTitle:
    """Create a new job title in the database."""
    new_job_title = JobTitle(name=job_title.name)
    db.add(new_job_title)
    db.commit()
    db.refresh(new_job_title)
    return new_job_title

def get_job_title_by_id(job_title_id: int, db: Session) -> JobTitle:
    """Retrieve a job title by ID."""
    return db.query(JobTitle).filter(JobTitle.id == job_title_id).first()

def update_job_title(
                job_title_id: int, job_title: JobTitleCreateSchema,
                db: Session,
            ) -> JobTitle:
    """Update an existing job title."""
    db_job_title = db.query(JobTitle).filter(JobTitle.id == job_title_id).first()
    if db_job_title:
        db_job_title.name = job_title.name
        db.commit()
        db.refresh(db_job_title)
    return db_job_title

def delete_job_title(job_title_id: int, db: Session) -> bool:
    """Delete a job title from the database."""
    db_job_title = db.query(JobTitle).filter(JobTitle.id == job_title_id).first()
    if db_job_title:
        db.delete(db_job_title)
        db.commit()
        return True
    return False

def get_employees_by_job_title(job_title_id: int, db: Session) -> list:
    """Retrieve all employees with the specified job title."""
    return db.query(Employee).filter(Employee.job_title_id == job_title_id).all()

def get_medium_salary_by_job_title(job_title_id: int, db: Session) -> float:
    """Calculate the average (medium) salary for employees with a specific job title.

    Args:
        job_title_id (int): The ID of the job title to filter employees by.
        db (Session): The database session used to query the database.

    Returns:
        float: The average salary of employees with the specified job title.
               Returns 0 if there are no employees with the given job title or
               if no salary records are found.

    """
    employees = get_employees_by_job_title(job_title_id, db)

    if not employees:
        return 0

    total_salary = 0
    total_employees = 0
    for employee in employees:

        latest_salary = employee_service.get_active_salary(employee.id, db)

        if latest_salary:
            total_salary += latest_salary.monthly_income
            total_employees += 1

    if total_employees == 0:
        return 0

    return round(total_salary / total_employees, 2)

def get_average_performance_score_by_job_title(job_title_id: int, db: Session) -> float:
    """Calculate the average performance score for employees with a specific job title.

    Args:
        job_title_id (int): The ID of the job title to filter employees by.
        db (Session): The database session to use for querying.

    Returns:
        float: The average performance score of employees with the specified job title.
        Returns 0 if there are no employees with the given job title or if no reviews
        are found.

    """
    employees = db.query(Employee).filter(Employee.job_title_id == job_title_id).all()

    if not employees:
        return 0

    total_score = 0
    total_reviews = 0
    for employee in employees:
        latest_review = employee_service.get_latest_performance_review(employee.id, db)
        if latest_review:
            total_score += latest_review.score
            total_reviews += 1

    if total_reviews == 0:
        return 0

    return round(total_score / total_reviews, 2)
