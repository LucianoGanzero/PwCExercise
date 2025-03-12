"""Module defines the status endpoints for the PwCExercise service.

Endpoints:
    - GET /health: Returns the health status of the service.
    - GET /version: Returns the version of the service.

"""
from fastapi import APIRouter
from fastapi.responses import JSONResponse

status_router = APIRouter()

@status_router.get("/health", tags=["status"])
def healthcheck() -> JSONResponse:
    """Health check endpoint that returns the status of the service."""
    return JSONResponse(content={"status": "Everything is OK"})

@status_router.get("/version", tags=["status"])
def version() -> JSONResponse:
    """Version endpoint that returns the version of the service."""
    return JSONResponse(content={"version": "1.0.0"})
