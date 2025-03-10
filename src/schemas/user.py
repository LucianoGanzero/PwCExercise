from __future__ import annotations

from pydantic import BaseModel


class User(BaseModel):
    id : int | None = None
    name: str
    email: str
