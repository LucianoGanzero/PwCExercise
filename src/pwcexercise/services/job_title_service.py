"""Provides services for managing job titles in the database."""

from sqlalchemy.orm import Session

from src.pwcexercise.models.job_title import JobTitle
from src.pwcexercise.schemas.job_title import JobTitleCreateSchema


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
