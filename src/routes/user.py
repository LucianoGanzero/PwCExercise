from fastapi import APIRouter
from src.config.db import conn
from src.models.user import users

user = APIRouter()

@user.get("/users")
def get_users():
    return conn.execute(users.select()).fetchall()
