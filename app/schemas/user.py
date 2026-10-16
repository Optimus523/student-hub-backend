from typing import Annotated
from pydantic import BaseModel, StringConstraints


# Input data required when creating a new user account.
class UserCreate(BaseModel):
    username: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=3,
            max_length=30,
            pattern=r"^[A-Za-z0-9_]+$",
            to_lower=True,
        ),
    ]
    password: Annotated[str, StringConstraints(min_length=8, max_length=128)]


# Public user data returned by the API after registration or login.
class UserPublic(BaseModel):
    id: int
    username: str
