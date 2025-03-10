from fastapi import FastAPI

from src.routes.employee import employee

app = FastAPI(
    title = "Exercise for PwC",
    description = "FastAPI with SQLAlchemy.",
    openapi_tags = [
        {
            "name": "employees",
            "description": "Operations related to employees.",
        },
    ],
)

app.include_router(employee, prefix="/employees")
