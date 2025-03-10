from sqlalchemy import Column, Table
from sqlalchemy.sql.sqltypes import Integer, String

from src.config.db import engine, meta

users = Table(
    "users",
    meta,
    Column("id", Integer, primary_key=True),
    Column("name", String(255)),
    Column("email", String(255)),
)

meta.create_all(engine)
