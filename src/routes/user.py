from fastapi import APIRouter, Response, status
from starlette.status import HTTP_204_NO_CONTENT

from src.config.db import conn
from src.models.user import users
from src.schemas.user import User

user = APIRouter()


@user.get("/users", response_model=list[User], tags=["users"])
def get_users() -> list:
    """Retrieve all users from the database.

    Returns:
        list: A list of all users.

    """
    return conn.execute(users.select()).fetchall()


@user.post("/users", response_model=User, tags=["users"])
def create_user(user: User) -> dict:
    """Create a new user in the database.

    Args:
        user (User): The user data to create.

    Returns:
        dict: The created user data.

    """
    new_user = {"name": user.name, "email": user.email}
    result = conn.execute(users.insert().values(new_user))
    return conn.execute(users.select().where(users.c.id == result.lastrowid)).first()


@user.get("/users/{user_id}", response_model=User, tags=["users"])
def get_user(user_id: int) -> dict:
    """Retrieve a user from the database by ID.

    Args:
        user_id (int): The ID of the user to retrieve.

    Returns:
        dict: The user data.

    """
    return conn.execute(users.select().where(users.c.id == user_id)).first()


@user.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def delete_user(user_id: int) -> Response:
    """Delete a user from the database by ID.

    Args:
        user_id (int): The ID of the user to delete.

    Returns:
        dict: An empty response with a 204 status code.

    """
    conn.execute(users.delete().where(users.c.id == user_id))
    return Response(status_code=HTTP_204_NO_CONTENT)


@user.put("/users/{user_id}", response_model=User, tags=["users"])
def update_user(user_id: int, user: User) -> dict:
    """Update a user in the database by ID.

    Args:
        user_id (int): The ID of the user to update.
        user (User): The new user data.

    Returns:
        dict: The updated user data.

    """
    conn.execute(users.update().where(users.c.id == user_id)
                .values(
                    name=user.name,
                    email=user.email,
                ))
    return conn.execute(users.select().where(users.c.id == user_id)).first()
