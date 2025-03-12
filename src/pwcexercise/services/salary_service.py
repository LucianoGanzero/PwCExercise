"""Provides services for managing salaries in the database."""
from datetime import datetime, timedelta, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from src.pwcexercise.models.salary import Salary
from src.pwcexercise.schemas.salary import SalaryCreateSchema
from src.pwcexercise.utils.logger import logger


def get_all_salaries(db: Session) -> list:
    """Retrieve all salaries from the database."""
    return db.query(Salary).all()

def create_salary(salary: SalaryCreateSchema, db: Session) -> Salary:
    """Create a new salary in the database."""
    new_salary = Salary(
        employee_id=salary.employee_id,
        monthly_income=salary.monthly_income,
        hourly_rate=salary.hourly_rate,
        effective_date=salary.effective_date,
    )
    db.add(new_salary)
    db.commit()
    db.refresh(new_salary)
    return new_salary

def get_salary_by_id(salary_id: int, db: Session) -> Salary:
    """Retrieve a salary by ID."""
    return db.query(Salary).filter(Salary.id == salary_id).first()

def update_salary(salary_id: int, salary: SalaryCreateSchema, db: Session) -> Salary:
    """Update a salary in the database by ID."""
    db.query(Salary).filter(Salary.id == salary_id).update(salary.dict())
    db.commit()
    return db.query(Salary).filter(Salary.id == salary_id).first()

def delete_salary(salary_id: int, db: Session) -> bool:
    """Delete a salary from the database by ID."""
    salary = db.query(Salary).filter(Salary.id == salary_id).first()
    if salary:
        db.delete(salary)
        db.commit()
        return True
    return False

def get_highest_salary_in_last_six_months(employee_id: int, db: Session) -> Salary:
    """Retrieve the highest salary in the last six months for the given employee."""
    six_months_ago = datetime.now(tz=timezone.utc) - timedelta(days=180)

    salaries = db.query(Salary).filter(
        Salary.employee_id == employee_id,
        Salary.effective_date >= six_months_ago,
    ).all()

    if not salaries:
        return None

    return max(salaries, key=lambda s: s.monthly_income)

def get_historic_average_salary(db: Session) -> float:
    """Get the average salary from the database."""
    avg_salary = db.query(Salary).with_entities(
        func.avg(Salary.monthly_income),
    ).scalar()
    return avg_salary if avg_salary is not None else 0.0

def get_current_average_salary(db: Session) -> float:
    """Get the average of the most recent salary for each employee."""
    subquery = (
        db.query(Salary.employee_id, func.max(Salary.effective_date).label("max_date"))
        .group_by(Salary.employee_id)
        .subquery()
    )

    current_salaries = (
        db.query(Salary.monthly_income)
        .join(subquery, (Salary.employee_id == subquery.c.employee_id)
        & (Salary.effective_date == subquery.c.max_date))
    )

    avg_salary = current_salaries.with_entities(
        func.avg(Salary.monthly_income),
    ).scalar()

    return avg_salary if avg_salary is not None else 0.0
