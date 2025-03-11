"""Module containing the JobTitle model.

The JobTitle model represents all the job titles in the organization.
"""

from sqlalchemy import Column, Integer, String

from .base import Base


class JobTitle(Base):
    """Job titles model representing all the job titles in the organization."""

    __tablename__ = "job_titles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
