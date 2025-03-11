"""Set up the FastAPI application with various routers."""

from fastapi import FastAPI

from src.pwcexercise.routes.department import department_router
from src.pwcexercise.routes.employee import employee
from src.pwcexercise.routes.job_title import job_title_router
from src.pwcexercise.routes.performance_review import performance_review_router
from src.pwcexercise.routes.salary import salary_router

app = FastAPI(
    title = "Exercise for PwC",
    description = "FastAPI with SQLAlchemy.",
    openapi_tags = [
        {
            "name": "employees",
            "description": "Operations related to employees.",
        },
        {
            "name": "departments",
            "description": "Operations related to departments.",
        },
        {
            "name": "performance_reviews",
            "description": "Operations related to performance reviews.",
        },
        {
            "name": "salaries",
            "description": "Operations related to salaries.",
        },
        {
            "name": "job_titles",
            "description": "Operations related to job titles",
        },
    ],
)

app.include_router(employee, prefix="/employees")
app.include_router(department_router, prefix="/departments")
app.include_router(performance_review_router, prefix="/performance_reviews")
app.include_router(salary_router, prefix="/salaries")
app.include_router(job_title_router, prefix="/job_titles")
