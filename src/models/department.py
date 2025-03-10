from sqlalchemy import Column, Integer, String

from .base import Base


class Department(Base):
    """Department model representing a department in the organization."""

    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
