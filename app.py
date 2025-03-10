from fastapi import FastAPI

from src.routes.user import user

app = FastAPI(
    title = "Exercise for PwC",
    description = "FastAPI with SQLAlchemy.",
    openapi_tags = [
        {
            "name": "users",
            "description": "Operations related to users.",
        },
    ],
)

app.include_router(user, prefix="/user")
