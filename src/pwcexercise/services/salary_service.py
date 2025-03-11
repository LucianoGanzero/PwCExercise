"""Provides services for managing salaries in the database."""

from sqlalchemy.orm import Session

from src.pwcexercise.models.salary import Salary
from src.pwcexercise.schemas.salary import SalaryCreateSchema


def get_all_salaries(db: Session) -> list:
    """Retrieve all salaries from the database."""
    return db.query(Salary).all()

def create_salary(salary: SalaryCreateSchema, db: Session) -> Salary:
    """Create a new salary in the database."""
    new_salary = Salary(
        employee_id=salary.employee_id,
        salary_amount=salary.salary_amount,
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
