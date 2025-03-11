"""Module containing the schema for department data."""

from pydantic import BaseModel


class DepartmentSchema(BaseModel):
    """Schema for department data."""

    id: int
    name: str

    class Config:
        """Configuration for the DepartmentSchema."""

        orm_mode = True
