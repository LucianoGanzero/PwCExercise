"""Module containing the schema for department data."""

from pydantic import BaseModel


class DepartmentCreateSchema(BaseModel):
    """Schema for department creation data."""

    name: str

    class Config:
        """Configuration for the DepartmentCreateSchema."""

        orm_mode = True

class DepartmentSchema(BaseModel):
    """Schema for department data."""

    id: int
    name: str

    class Config:
        """Configuration for the DepartmentSchema."""

        orm_mode = True
