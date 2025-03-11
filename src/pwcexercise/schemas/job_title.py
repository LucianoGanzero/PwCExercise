"""Module containing the schema for job title data."""

from pydantic import BaseModel


class JobTitleSchema(BaseModel):
    """Schema for job title data."""

    id: int
    name: str

    class Config:
        """Configuration for the JobTitleSchema."""

        orm_mode = True
