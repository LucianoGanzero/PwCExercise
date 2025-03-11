from pydantic import BaseModel


class DepartmentSchema(BaseModel):
    """Schema for department data."""

    id: int
    name: str

    class Config:
        orm_mode = True
