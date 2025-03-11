from fastapi import FastAPI

from src.routes.department import department_router
from src.routes.employee import employee

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
    ],
)

app.include_router(employee, prefix="/employees")
app.include_router(department_router, prefix="/departments")
