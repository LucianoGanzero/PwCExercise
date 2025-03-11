import random
from datetime import date, timedelta

from sqlalchemy.orm import Session

from src.pwcexercise.models.department import Department
from src.pwcexercise.models.employee import Employee
from src.pwcexercise.models.job_title import JobTitle
from src.pwcexercise.models.performance_review import PerformanceReview
from src.pwcexercise.models.salary import Salary


def seed_departments(session: Session, df):
    departments = set(df["Department"].dropna().unique())
    for name in departments:
        session.add(Department(name=name))
    session.commit()

def seed_job_titles(session: Session, df):
    job_titles = set(df["JobRole"].dropna().unique())
    for name in job_titles:
        session.add(JobTitle(name=name))
    session.commit()

def seed_employees(session: Session, df):
    departments = {d.name: d.id for d in session.query(Department).all()}
    job_titles = {j.name: j.id for j in session.query(JobTitle).all()}
    for _, row in df.iterrows():
        hire_date = date.today() - timedelta(days=row["YearsAtCompany"] * 365)
        employee = Employee(
            emp_id=row["EmpID"],
            age=row["Age"],
            department_id=departments.get(row["Department"]),
            hire_date=hire_date,
            job_title_id=job_titles.get(row["JobRole"]),
            hourly_rate=row["HourlyRate"]
        )
        session.add(employee)
    session.commit()

def seed_salaries(session: Session, df):
    employees = {e.emp_id: e.id for e in session.query(Employee).all()}
    for _, row in df.iterrows():
        if row["EmpID"] in employees:
            effective_date = date.today() - timedelta(days=row["YearsSinceLastPromotion"] * 365)
            salary = Salary(
                employee_id=employees[row["EmpID"]],
                salary_amount=row["MonthlyIncome"],
                effective_date=effective_date
            )
            session.add(salary)
    session.commit()

def seed_performance_reviews(session: Session, df):
    employees = {e.emp_id: e.id for e in session.query(Employee).all()}
    for _, row in df.iterrows():
        if row["EmpID"] in employees:
            review = PerformanceReview(
                employee_id=employees[row["EmpID"]],
                review_date=date.today() - timedelta(days=random.randint(30, 365 * 2)),
                score=row.get("PerformanceRating", 3),
                comments="Auto-generated review"
            )
            session.add(review)
    session.commit()

def seed_database(session: Session, df):
    seed_departments(session, df)
    seed_job_titles(session, df)
    seed_employees(session, df)
    seed_salaries(session, df)
    seed_performance_reviews(session, df)